# validate_ood.py
"""
Usage:
  python validate_ood.py PATH_TO_KNOWN_DIR PATH_TO_OOD_DIR \
      --model model/fruit_type_convnext_tiny_best.keras \
      --size 224
Example:
  python validate_ood.py val_known val_ood --model model/fruit_type_convnext_tiny_best.keras
"""

import os, sys, argparse, json, numpy as np
from PIL import Image

try:
    import tensorflow as tf
    from tensorflow.keras.applications.convnext import preprocess_input as convnext_preprocess
except Exception:
    tf = None
    convnext_preprocess = None

def load_image(path, target_size=(224,224), preprocess_func=None):
    img = Image.open(path).convert("RGB").resize(target_size)
    arr = np.array(img).astype("float32")
    arr = np.expand_dims(arr, 0)
    if preprocess_func:
        try:
            arr = preprocess_func(arr)
        except Exception:
            arr = arr / 255.0
    else:
        arr = arr / 255.0
    return arr

def gather_files(root):
    exts = {".jpg",".jpeg",".png"}
    files=[]
    for r,_,fnames in os.walk(root):
        for f in fnames:
            if os.path.splitext(f)[1].lower() in exts:
                files.append(os.path.join(r,f))
    return sorted(files)

def main(args):
    if tf is None:
        print("ERROR: TensorFlow not available in this environment. Activate venv with TF installed.")
        return

    model_path = args.model
    if not os.path.exists(model_path):
        print("Model not found:", model_path)
        return

    print("Loading model:", model_path)
    model = tf.keras.models.load_model(model_path, compile=False)
    print("Model loaded. Input shape:", getattr(model, "input_shape", None))

    known_files = gather_files(args.known)
    ood_files = gather_files(args.ood)
    print("Known images:", len(known_files), "OOD images:", len(ood_files))
    if len(known_files)==0:
        print("No known images found. Exiting.")
        return

    known_conf = []
    for i,fp in enumerate(known_files,1):
        try:
            x = load_image(fp, target_size=(args.size,args.size), preprocess_func=convnext_preprocess)
            preds = model.predict(x, verbose=0)
            probs = preds[0] if preds.ndim>1 else preds.flatten()
            known_conf.append(float(np.max(probs)))
        except Exception as e:
            print("Skip known:", fp, "err:", e)

    ood_conf = []
    for i,fp in enumerate(ood_files,1):
        try:
            x = load_image(fp, target_size=(args.size,args.size), preprocess_func=convnext_preprocess)
            preds = model.predict(x, verbose=0)
            probs = preds[0] if preds.ndim>1 else preds.flatten()
            ood_conf.append(float(np.max(probs)))
        except Exception as e:
            print("Skip ood:", fp, "err:", e)

    known_conf = np.array(known_conf) if len(known_conf)>0 else np.array([])
    ood_conf = np.array(ood_conf) if len(ood_conf)>0 else np.array([])

    def show_stats(name, arr):
        if arr.size==0:
            print(f"{name}: NONE")
            return
        print(f"{name}: n={arr.size} min={arr.min():.4f} 5%={np.percentile(arr,5):.4f} mean={arr.mean():.4f} 95%={np.percentile(arr,95):.4f} max={arr.max():.4f}")

    show_stats("KNOWN conf", known_conf)
    show_stats("OOD conf", ood_conf)

    # Evaluate thresholds and report TPR and FPR
    ths = np.linspace(0.0,1.0,101)
    rows=[]
    for t in ths:
        tpr = (known_conf >= t).mean() if known_conf.size else 0.0  # >= threshold -> accepted as known
        fpr = (ood_conf >= t).mean() if ood_conf.size else 0.0     # fraction of OOD that would be accepted (bad)
        rows.append((t, tpr, fpr))

    # Find candidate threshold with TPR>=0.95 and FPR<=0.05
    candidate = None
    for t, tpr, fpr in rows:
        if tpr >= 0.95 and fpr <= 0.05:
            candidate = (t, tpr, fpr)
            break

    if candidate:
        print("\nRecommended threshold (TPR>=0.95 & FPR<=0.05):", candidate)
    else:
        # find best tradeoff maximizing (TPR - FPR)
        best = max(rows, key=lambda x: (x[1]-x[2], x[1], -x[2]))
        print("\nNo threshold met TPR>=0.95 and FPR<=0.05.")
        print("Best tradeoff threshold (max TPR-FPR):", best)

    # Print a short table for human review
    print("\nThreshold  TPR    FPR")
    for t,tpr,fpr in rows[::5]:   # show every 5th for brevity
        print(f"{t:0.2f}      {tpr:.3f}  {fpr:.3f}")

    # Save confidences for later plotting
    out = {"known_conf": known_conf.tolist(), "ood_conf": ood_conf.tolist()}
    with open("confidences_summary.json", "w") as f:
        json.dump(out, f)
    print("\nSaved confidences_summary.json")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("known", help="path to known fruit images folder (val_known)")
    p.add_argument("ood", help="path to OOD images folder (val_ood)")
    p.add_argument("--model", default="model/fruit_type_convnext_tiny_best.keras", help="path to type model (.keras/.h5)")
    p.add_argument("--size", type=int, default=224, help="image size for the model")
    args = p.parse_args()
    main(args)
