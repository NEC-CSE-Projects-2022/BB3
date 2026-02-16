# app.py — complete file with /validate endpoint and OOD checks

import os
import os
import json
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import tensorflow as tf
import kagglehub
import zipfile
import shutil

# ---------------- CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
REJECT_FOLDER = os.path.join(UPLOAD_FOLDER, "rejected")
ANALYSIS_FILE = os.path.join(BASE_DIR, "analysis_results.json")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REJECT_FOLDER, exist_ok=True)

# Thresholds (tweak if needed)
TYPE_THRESHOLD = 0.70       # require >=70% confidence to accept type
QUALITY_THRESHOLD = 0.70    # require >=70% confidence to accept quality

# Filenames (edit if your files have different names)
TYPE_MODEL_FILE = os.path.join(MODEL_DIR, "convnext_tiny_best.keras")
QUALITY_MODEL_FILE = os.path.join(MODEL_DIR, "best_effnetv2b0_quality.keras")
TYPE_MAP_FILE = os.path.join(MODEL_DIR, "type_class_mapping.json")
QUALITY_MAP_FILE = os.path.join(MODEL_DIR, "quality_class_mapping.json")

ALLOWED_EXT = {"png", "jpg", "jpeg"}
MAX_CONTENT_LENGTH = 6 * 1024 * 1024  # 6 MB

# ---------------- APP ----------------
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.config["SECRET_KEY"] = "replace_with_a_strong_secret"

# ---------------- HELPERS ----------------
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print("[WARNING] Failed to load mapping:", path)
        return None

type_labels = load_json(TYPE_MAP_FILE) or []
quality_labels = load_json(QUALITY_MAP_FILE) or []

def safe_load_model(path):
    if not os.path.exists(path):
        print("[ERROR] Model not found:", path)
        return None
    try:
        print(f"[INFO] Loading model from: {path}")
        m = tf.keras.models.load_model(path, compile=False)
        print("[OK] Loaded model successfully:", path)
        try:
            print(f"   Input shape: {m.input_shape}, Output shape: {m.output_shape}")
        except Exception:
            pass
        return m
    except Exception as e:
        print(f"[ERROR] Failed to load model {path}: {e}")
        import traceback
        traceback.print_exc()
        return None

type_model = safe_load_model(TYPE_MODEL_FILE)
quality_model = safe_load_model(QUALITY_MODEL_FILE)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

def save_analysis_result(filename, fruit_type, type_conf, quality, quality_conf, valid_any):
    """Save analysis result to JSON file"""
    try:
        # Load existing results
        if os.path.exists(ANALYSIS_FILE):
            with open(ANALYSIS_FILE, 'r') as f:
                results = json.load(f)
        else:
            results = {}
        
        # Add new result
        results[filename] = {
            'fruit_type': fruit_type,
            'type_conf': type_conf,
            'quality': quality,
            'quality_conf': quality_conf,
            'valid_any': valid_any,
            'timestamp': os.path.getmtime(os.path.join(UPLOAD_FOLDER, filename)) if os.path.exists(os.path.join(UPLOAD_FOLDER, filename)) else 0
        }
        
        # Save results
        with open(ANALYSIS_FILE, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"[INFO] Saved analysis result for {filename}")
    except Exception as e:
        print(f"[ERROR] Failed to save analysis result: {e}")

def load_analysis_result(filename):
    """Load analysis result from JSON file"""
    try:
        if os.path.exists(ANALYSIS_FILE):
            with open(ANALYSIS_FILE, 'r') as f:
                results = json.load(f)
            return results.get(filename, None)
    except Exception as e:
        print(f"[ERROR] Failed to load analysis result: {e}")
    return None

def preprocess_image(img_path, target_size=(224,224), preprocess_func=None):
    try:
        # Check if file exists and is readable
        if not os.path.exists(img_path):
            print(f"[ERROR] Image file not found: {img_path}")
            return None
            
        # Open and validate image
        img = Image.open(img_path)
        print(f"[DEBUG] Image loaded: {img_path}, mode: {img.mode}, size: {img.size}")
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert("RGB")
            print(f"[DEBUG] Converted to RGB")
        
        # Resize image
        img = img.resize(target_size)
        print(f"[DEBUG] Resized to: {target_size}")
        
        # Convert to numpy array
        arr = np.array(img).astype("float32")
        print(f"[DEBUG] Array shape: {arr.shape}, dtype: {arr.dtype}, range: [{arr.min():.2f}, {arr.max():.2f}]")
        
        # Add batch dimension
        arr = np.expand_dims(arr, 0)
        
        # Validate array shape and values
        if arr.size == 0:
            print("[ERROR] Empty image array")
            return None
            
        if np.isnan(arr).any() or np.isinf(arr).any():
            print("[ERROR] Invalid values in image array")
            return None
        
        # Apply preprocessing function if provided
        if preprocess_func:
            try:
                arr = preprocess_func(arr)
                print(f"[SUCCESS] Applied {preprocess_func.__name__} preprocessing")
                print(f"[DEBUG] After preprocessing - shape: {arr.shape}, range: [{arr.min():.2f}, {arr.max():.2f}]")
            except Exception as e:
                print(f"[WARNING] Preprocessing failed: {e}, using basic normalization")
                arr = arr / 255.0
        else:
            arr = arr / 255.0
            
        # Final validation
        print(f"[INFO] Processed image shape: {arr.shape}, dtype: {arr.dtype}")
        print(f"[INFO] Min/Max values: {arr.min():.4f}/{arr.max():.4f}")
        
        return arr
        
    except Exception as e:
        print(f"[ERROR] Failed to preprocess image {img_path}: {e}")
        import traceback
        traceback.print_exc()
        return None

# optional official preprocessors
try:
    from tensorflow.keras.applications.efficientnet import preprocess_input as eff_preprocess
    print("[OK] Loaded EfficientNet preprocessor")
except Exception as e:
    print(f"[WARNING] Failed to load EfficientNet preprocessor: {e}")
    eff_preprocess = None

try:
    from tensorflow.keras.applications.convnext import preprocess_input as convnext_preprocess
    print("[OK] Loaded ConvNeXt preprocessor")
except Exception as e:
    print(f"[WARNING] Failed to load ConvNeXt preprocessor: {e}")
    convnext_preprocess = None

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    # Redirect to multiple page (new home)
    return redirect(url_for("multiple"))

@app.route("/multiple")
def multiple():
    # Multiple images upload page (now the home page)
    return render_template("multiple.html")

@app.route("/history")
def history():
    # Get all analysis results from uploads folder
    analyses = []
    
    try:
        # Scan uploads folder for images
        upload_folder = app.config["UPLOAD_FOLDER"]
        for filename in os.listdir(upload_folder):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Try to load saved analysis result
                result = load_analysis_result(filename)
                
                if result:
                    # Use saved analysis result
                    analysis = {
                        'id': filename,
                        'image_path': f"static/uploads/{filename}",
                        'fruit_type': result['fruit_type'],
                        'type_conf': result['type_conf'],
                        'quality': result['quality'],
                        'quality_conf': result['quality_conf'],
                        'valid_any': result['valid_any']
                    }
                else:
                    # Fallback: run quick analysis for existing images without saved results
                    try:
                        img_path = os.path.join(upload_folder, filename)
                        
                        # Type prediction
                        x_type = preprocess_image(img_path, target_size=(224,224), preprocess_func=convnext_preprocess)
                        
                        if x_type is not None and type_model is not None:
                            preds_type = type_model.predict(x_type)
                            probs_type = preds_type[0] if preds_type.ndim > 1 else preds_type.flatten()
                            max_idx = int(np.argmax(probs_type))
                            max_conf = float(np.max(probs_type))
                            
                            print(f"[DEBUG] Type predictions - Raw: {probs_type}")
                            print(f"[DEBUG] Type predictions - Max index: {max_idx}, confidence: {max_conf:.4f}")
                            print(f"[DEBUG] Type labels available: {type_labels}")
                            print(f"[DEBUG] Predicted class: {type_labels[max_idx] if max_idx < len(type_labels) else 'Unknown'}")
                            
                            if max_conf >= TYPE_THRESHOLD:
                                fruit_type = type_labels[max_idx] if max_idx < len(type_labels) else f"Class_{max_idx}"
                                valid_any = True
                                print(f"[INFO] Valid prediction: {fruit_type} at {max_conf:.4f}")
                            else:
                                fruit_type = "Invalid Image"
                                valid_any = False
                                print(f"[INFO] Low confidence prediction: INVALID at {max_conf:.4f}")
                                max_conf = 0.0
                        else:
                            fruit_type = "Unknown"
                            max_conf = 0.0
                            valid_any = False
                        
                        # Quality prediction (only if type is valid)
                        if valid_any and quality_model is not None:
                            x_q = preprocess_image(img_path, target_size=(224,224), preprocess_func=eff_preprocess)
                            if x_q is not None:
                                try:
                                    preds_q = quality_model.predict(x_q)
                                    probs_q = preds_q[0] if preds_q.ndim > 1 else preds_q.flatten()
                                    max_q_idx = int(np.argmax(probs_q))
                                    max_q_conf = float(np.max(probs_q))
                                    
                                    print(f"[DEBUG] {filename} - Quality predictions: {probs_q}")
                                    print(f"[DEBUG] {filename} - Quality max idx: {max_q_idx}, conf: {max_q_conf}")
                                    print(f"[DEBUG] {filename} - Quality labels: {quality_labels}")
                                    
                                    if max_q_conf >= QUALITY_THRESHOLD:
                                        quality = quality_labels[max_q_idx] if max_q_idx < len(quality_labels) else f"Class_{max_q_idx}"
                                        quality_conf = round(max_q_conf * 100, 2)
                                        print(f"[DEBUG] {filename} - Final quality: {quality} ({quality_conf}%)")
                                    else:
                                        quality = "Invalid"
                                        quality_conf = round(max_q_conf * 100, 2)
                                        print(f"[DEBUG] {filename} - Quality below threshold: {quality} ({quality_conf}%)")
                                except Exception as e:
                                    print(f"[ERROR] Quality prediction failed for {filename}: {e}")
                                    quality = "Unknown"
                                    quality_conf = 0.0
                            else:
                                quality = "Unknown"
                                quality_conf = 0.0
                                print(f"[DEBUG] {filename} - Quality preprocessing failed")
                        else:
                            quality = "Invalid Image" if not valid_any else "Unknown"
                            quality_conf = 0.0
                            print(f"[DEBUG] {filename} - Quality prediction skipped (valid_any: {valid_any}, quality_model: {quality_model is not None})")
                        
                        analysis = {
                            'id': filename,
                            'image_path': f"static/uploads/{filename}",
                            'fruit_type': fruit_type,
                            'type_conf': round(max_conf * 100, 2),
                            'quality': quality,
                            'quality_conf': quality_conf,
                            'valid_any': valid_any
                        }
                        
                        # Save the result for future use
                        save_analysis_result(filename, fruit_type, analysis['type_conf'], quality, analysis['quality_conf'], valid_any)
                        
                    except Exception as e:
                        print(f"[ERROR] Failed to analyze {filename}: {e}")
                        analysis = {
                            'id': filename,
                            'image_path': f"static/uploads/{filename}",
                            'fruit_type': 'Unknown',
                            'type_conf': 0.0,
                            'quality': 'Unknown',
                            'quality_conf': 0.0,
                            'valid_any': False
                        }
                
                analyses.append(analysis)
        
        # Also scan rejected folder
        rejected_folder = REJECT_FOLDER
        if os.path.exists(rejected_folder):
            for filename in os.listdir(rejected_folder):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    result = load_analysis_result(filename)
                    
                    if result:
                        analysis = {
                            'id': filename,
                            'image_path': f"static/uploads/rejected/{filename}",
                            'fruit_type': result['fruit_type'],
                            'type_conf': result['type_conf'],
                            'quality': result['quality'],
                            'quality_conf': result['quality_conf'],
                            'valid_any': result['valid_any']
                        }
                    else:
                        analysis = {
                            'id': filename,
                            'image_path': f"static/uploads/rejected/{filename}",
                            'fruit_type': 'Invalid',
                            'type_conf': 0.0,
                            'quality': 'Invalid',
                            'quality_conf': 0.0,
                            'valid_any': False
                        }
                    
                    analyses.append(analysis)
                    
    except Exception as e:
        print(f"[ERROR] Failed to load history: {e}")
    
    # Sort by filename (newest first)
    analyses.sort(key=lambda x: x['id'], reverse=True)
    
    return render_template("history.html", analyses=analyses)

@app.route("/delete_analysis/<filename>", methods=["DELETE"])
def delete_analysis(filename):
    """Delete an analysis result and associated image file"""
    try:
        # Secure the filename
        filename = secure_filename(filename)
        
        # Delete from uploads folder
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(upload_path):
            os.remove(upload_path)
            print(f"[INFO] Deleted upload: {upload_path}")
        
        # Delete from rejected folder
        reject_path = os.path.join(REJECT_FOLDER, filename)
        if os.path.exists(reject_path):
            os.remove(reject_path)
            print(f"[INFO] Deleted rejected: {reject_path}")
        
        # Remove from analysis results
        remove_analysis_result(filename)
        
        return jsonify({"success": True, "message": "Analysis deleted successfully"})
        
    except Exception as e:
        print(f"[ERROR] Failed to delete analysis {filename}: {e}")
        return jsonify({"success": False, "message": "Failed to delete analysis"}), 500

def remove_analysis_result(filename):
    """Remove analysis result from JSON file"""
    try:
        if os.path.exists(ANALYSIS_FILE):
            with open(ANALYSIS_FILE, 'r', encoding='utf-8') as f:
                analyses = json.load(f)
            
            # Remove the analysis with matching filename
            analyses = [a for a in analyses if a.get('filename') != filename]
            
            # Save updated analyses
            with open(ANALYSIS_FILE, 'w', encoding='utf-8') as f:
                json.dump(analyses, f, indent=2)
                
            print(f"[INFO] Removed analysis result for: {filename}")
            
    except Exception as e:
        print(f"[ERROR] Failed to remove analysis result: {e}")

@app.route("/samples")
def samples():
    # samples page with sample images
    return render_template("samples.html")

@app.route("/dataset")
def dataset():
    # dataset information page
    return render_template("dataset.html")

@app.route("/download_dataset")
def download_dataset():
    """Download the latest version of dataset from Kaggle and organize sample images"""
    try:
        # Download latest version
        print("[INFO] Starting dataset download from Kaggle...")
        path = kagglehub.dataset_download("shashwatwork/fruitnet-indian-fruits-dataset-with-quality")
        
        print(f"[INFO] Dataset downloaded to: {path}")
        
        # Create samples folder
        samples_folder = os.path.join(BASE_DIR, "static", "samples")
        os.makedirs(samples_folder, exist_ok=True)
        
        # Copy sample images (first few of each type and quality)
        fruit_types = ["Apple", "Banana", "Guava", "Lemon", "Lime", "Orange", "Pomegranate"]
        quality_levels = ["Good Quality_Fruits", "Bad Quality_Fruits", "Mixed Qualit_Fruits"]
        
        samples_copied = 0
        
        for fruit in fruit_types:
            fruit_path = os.path.join(path, fruit)
            if os.path.exists(fruit_path):
                # Copy good, bad, and mixed quality samples for each fruit
                for quality in quality_levels:
                    quality_path = os.path.join(fruit_path, quality)
                    if os.path.exists(quality_path):
                        # Get first few images from each quality folder
                        images = [f for f in os.listdir(quality_path) 
                                 if f.lower().endswith(('.jpg', '.jpeg', '.png'))][:3]
                        
                        for img in images:
                            src_path = os.path.join(quality_path, img)
                            # Create organized filename
                            dst_name = f"{fruit.lower()}_{quality.lower().replace('_fruits', '').replace(' qualit', ' qualit')}_{img}"
                            dst_path = os.path.join(samples_folder, dst_name)
                            
                            # Copy image
                            shutil.copy2(src_path, dst_path)
                            samples_copied += 1
                            print(f"[INFO] Copied: {dst_name}")
        
        print(f"[INFO] Total sample images copied: {samples_copied}")
        
        # Create a zip file of samples
        zip_path = os.path.join(BASE_DIR, "fruit_samples.zip")
        
        if os.path.exists(zip_path):
            os.remove(zip_path)
        
        # Create zip file
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(samples_folder):
                for file in files:
                    if file.endswith(('.jpg', '.jpeg', '.png')):
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, samples_folder)
                        zipf.write(file_path, arcname)
        
        print(f"[INFO] Samples zipped to: {zip_path}")
        
        # Send the zip file to user
        return send_file(
            zip_path,
            as_attachment=True,
            download_name="fruit_quality_samples.zip",
            mimetype='application/zip'
        )
        
    except Exception as e:
        print(f"[ERROR] Failed to prepare samples: {e}")
        flash("Failed to prepare sample images. Please try again.", "danger")
        return redirect(url_for('dataset'))

@app.route("/quality/<fruit>")
def fruit_quality(fruit):
    # quality page for specific fruit
    return render_template("quality.html", fruit_name=fruit)

# Lightweight validation endpoint — used by client JS on file selection
@app.route('/validate', methods=['POST'])
def validate_image():
    """
    Receives a single file (FormData 'image'), runs the type_model only,
    returns JSON: { valid: bool, label: str, confidence: float }.
    """
    if 'image' not in request.files:
        return jsonify({"error": "no file"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "invalid extension"}), 400

    # Save temporary file
    filename = secure_filename(file.filename)
    tmp_path = os.path.join(app.config['UPLOAD_FOLDER'], "tmp_validate_" + filename)
    try:
        file.save(tmp_path)
    except Exception as e:
        return jsonify({"error": "save_failed", "detail": str(e)}), 500

    if type_model is None:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
        return jsonify({"error": "type model not loaded"}), 500

    # Preprocess & predict using type model
    x_type = preprocess_image(tmp_path, target_size=(224,224), preprocess_func=convnext_preprocess)
    if x_type is None:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
        return jsonify({"error": "Failed to process image"}), 500
        
    try:
        preds = type_model.predict(x_type)
        probs = preds[0] if preds.ndim > 1 else preds.flatten()
        top_idx = int(np.argmax(probs))
        top_conf = float(np.max(probs))
        label = type_labels[top_idx] if top_idx < len(type_labels) else f"Class_{top_idx}"
    except Exception as e:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
        return jsonify({"error": "prediction_failed", "detail": str(e)}), 500

    # cleanup
    try:
        os.remove(tmp_path)
    except Exception:
        pass

    valid = top_conf >= TYPE_THRESHOLD

    return jsonify({
        "valid": bool(valid),
        "label": label,
        "confidence": float(top_conf)
    }), 200

@app.route("/predict", methods=["POST"])
def predict():
    # Full predict flow (type + quality). Uses thresholds to mark invalid image.
    # Handle multiple files
    if "image" not in request.files:
        flash("No file uploaded!", "danger")
        return redirect(url_for("index"))

    files = request.files.getlist("image")
    if not files or files[0].filename == "":
        flash("No file selected!", "warning")
        return redirect(url_for("index"))

    # Limit to 10 files
    if len(files) > 10:
        flash("Maximum 10 files allowed at once!", "danger")
        return redirect(url_for("index"))

    results = []
    
    for file in files:
        if not allowed_file(file.filename):
            flash(f"File {file.filename} is not allowed (png/jpg/jpeg only)!", "danger")
            continue

        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        
        # If file exists, we will overwrite (that's fine for uploads)
        file.save(save_path)
        print(f"[UPLOADED] Uploaded: {save_path}")

        print(f"[INFO] Type model loaded: {type_model is not None}")
        print(f"[INFO] Quality model loaded: {quality_model is not None}")
        print(f"[INFO] Type labels loaded: {len(type_labels)} labels - {type_labels}")
        print(f"[INFO] Quality labels loaded: {len(quality_labels)} labels - {quality_labels}")
        print(f"[INFO] Current thresholds: TYPE={TYPE_THRESHOLD}, QUALITY={QUALITY_THRESHOLD}")

        # Type prediction
        if type_model is None:
            print("[ERROR] Type model not loaded - marking as invalid")
            type_label = "Invalid Image"
            type_conf = 0.0
        else:
            print("[INFO] Using actual type model for prediction")

        x_type = preprocess_image(save_path, target_size=(224,224), preprocess_func=convnext_preprocess)
        
        if x_type is None or type_model is None:
            print("[ERROR] Type preprocessing or model failed")
            type_label = "Invalid Image"
            type_conf = 0.0
        else:
            try:
                preds_type = type_model.predict(x_type, verbose=0)
                probs_type = preds_type[0] if preds_type.ndim > 1 else preds_type.flatten()
                max_idx = int(np.argmax(probs_type))
                max_conf = float(np.max(probs_type))
                
                print(f"[DEBUG] Type prediction - max_idx: {max_idx}, max_conf: {max_conf:.4f}")
                print(f"[DEBUG] All probabilities: {probs_type}")
                print(f"[DEBUG] Available labels: {type_labels}")
                print(f"[DEBUG] Threshold check: {max_conf:.4f} >= {TYPE_THRESHOLD} = {max_conf >= TYPE_THRESHOLD}")
                
                # Check if confidence is high enough for valid fruit
                print(f"[DEBUG] BEFORE CHECK: max_idx={max_idx}, len(type_labels)={len(type_labels)}")
                print(f"[DEBUG] BEFORE CHECK: max_conf={max_conf:.4f}, TYPE_THRESHOLD={TYPE_THRESHOLD}")
                print(f"[DEBUG] BEFORE CHECK: condition1={max_idx < len(type_labels)}, condition2={max_conf >= TYPE_THRESHOLD}")
                
                # FORCE INVALID DETECTION - SIMPLIFIED AND GUARANTEED
                if max_conf < TYPE_THRESHOLD:  # Use the same threshold as defined above
                    type_label = "Invalid Image"
                    type_conf = round(max_conf * 100, 2)
                    print(f"[FORCE] Invalid image: confidence {max_conf:.4f} < {TYPE_THRESHOLD}")
                elif max_idx < len(type_labels):
                    type_label = type_labels[max_idx]
                    type_conf = round(max_conf * 100, 2)
                    print(f"[SUCCESS] Valid fruit: {type_label} at {type_conf}%")
                else:
                    type_label = "Invalid Image"
                    type_conf = round(max_conf * 100, 2)
                    print(f"[ERROR] Index out of range")
                
            except Exception as e:
                print(f"[ERROR] Type prediction failed: {e}")
                type_label = "Invalid Image"
                type_conf = 0.0

        # Quality prediction
        if quality_model is None:
            print("[ERROR] Quality model not loaded - marking as invalid")
            quality_label = "Invalid Image"
            quality_conf = 0.0
        else:
            print("[INFO] Using actual quality model for prediction")

        x_q = preprocess_image(save_path, target_size=(224,224), preprocess_func=eff_preprocess)
        
        if x_q is None or quality_model is None:
            print("[ERROR] Quality preprocessing or model failed")
            quality_label = "Invalid Image"
            quality_conf = 0.0
        else:
            try:
                preds_q = quality_model.predict(x_q, verbose=0)
                probs_q = preds_q[0] if preds_q.ndim > 1 else preds_q.flatten()
                max_q_idx = int(np.argmax(probs_q))
                max_q_conf = float(np.max(probs_q))
                
                print(f"[DEBUG] Quality prediction - max_idx: {max_q_idx}, max_conf: {max_q_conf:.4f}")
                print(f"[DEBUG] Available quality labels: {quality_labels}")
                
                # If type is invalid, quality should also be invalid
                if type_label == "Invalid Image":
                    quality_label = "Invalid Image"
                    quality_conf = 0.0
                    print(f"[INFO] Type was invalid, marking quality as invalid too")
                # Check if confidence is high enough for valid quality
                elif max_q_idx < len(quality_labels) and max_q_conf >= QUALITY_THRESHOLD:
                    quality_label = quality_labels[max_q_idx]
                    quality_conf = round(max_q_conf * 100, 2)
                    print(f"[SUCCESS] Valid quality: {quality_label} at {quality_conf}%")
                else:
                    quality_label = "Invalid Image"
                    quality_conf = round(max_q_conf * 100, 2)
                    print(f"[INFO] Invalid quality detected: confidence {max_q_conf:.4f} < threshold {QUALITY_THRESHOLD}")
                
            except Exception as e:
                print(f"[ERROR] Quality prediction failed: {e}")
                quality_label = "Invalid Image"
                quality_conf = 0.0

        # ---- Render Result ----
        # Proper invalid detection - show Invalid Image for actual invalid images
        invalid_type = (type_label == "Invalid Image")
        invalid_quality = (quality_label == "Invalid Image")
        invalid_any = invalid_type or invalid_quality  # Invalid if EITHER fails

        result = {
            'filename': os.path.basename(save_path),
            'fruit_type': type_label,
            'type_conf': type_conf,
            'quality': quality_label,
            'quality_conf': quality_conf,
            'invalid_any': invalid_any,
            'invalid_type': invalid_type,
            'invalid_quality': invalid_quality
        }
        
        # Save analysis result to JSON file
        save_analysis_result(result['filename'], type_label, type_conf, quality_label, quality_conf, not invalid_any)
        
        results.append(result)

    # If only one file, render single result page
    if len(results) == 1:
        return render_template(
            "result.html",
            filename=results[0]['filename'],
            fruit_type=results[0]['fruit_type'],
            type_conf=results[0]['type_conf'],
            quality=results[0]['quality'],
            quality_conf=results[0]['quality_conf'],
            invalid_any=results[0]['invalid_any'],
            invalid_type=results[0]['invalid_type'],
            invalid_quality=results[0]['invalid_quality']
        )
    else:
        # Multiple files - render batch results page
        return render_template("batch_results.html", results=results)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    # serve uploaded image from static/uploads or rejected folder
    try:
        # First try normal uploads folder
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(upload_path):
            return redirect(url_for("static", filename="uploads/" + filename))
        
        # If not in uploads, try rejected folder
        rejected_path = os.path.join(REJECT_FOLDER, filename)
        if os.path.exists(rejected_path):
            return redirect(url_for("static", filename="uploads/rejected/" + filename))
        
        # If file not found anywhere, return 404
        return "File not found", 404
        
    except Exception as e:
        print(f"[ERROR] Failed to serve file {filename}: {e}")
        return "File not found", 404

if __name__ == "__main__":
    # Fix URL generation issues and use different port
    app.config.update(
        SERVER_NAME='127.0.0.1:8000',
        APPLICATION_ROOT='/',
        PREFERRED_URL_SCHEME='http',
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax'
    )
    
    # Run with explicit HTTP configuration on port 8000
    app.run(
        debug=True,
        host='127.0.0.1',
        port=8000,
        ssl_context=None  # Disable SSL
    )
