# inspect_h5.py
import json, h5py, sys, os
h5path = sys.argv[1] if len(sys.argv) > 1 else "model/convnext_tiny_best.keras"
print("Inspecting:", h5path, "| exists:", os.path.exists(h5path))
if not os.path.exists(h5path):
    sys.exit(1)
with h5py.File(h5path, 'r') as f:
    print("Top groups:", list(f.keys()))
    if 'model_config' in f.attrs:
        try:
            cfg = json.loads(f.attrs['model_config'].decode('utf-8'))
            layers = []
            def walk(node):
                if isinstance(node, dict):
                    if node.get('class_name'):
                        layers.append(node['class_name'])
                    for v in node.values():
                        walk(v)
                elif isinstance(node, list):
                    for v in node: walk(v)
            walk(cfg)
            print("Layer class names (unique):")
            print(sorted(set(layers)))
        except Exception as e:
            print("Failed to parse model_config:", e)
    else:
        print("No 'model_config' in H5 attributes.")
