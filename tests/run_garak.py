import logging
import os
import sys

# Configure logging to see output
logging.basicConfig(level=logging.INFO)

# Ensure project root is in path
# Ensure project root is in path
sys.path.insert(0, os.getcwd())

import importlib  # noqa: E402

from garak.harnesses.base import Harness  # noqa: E402
from garak.probes.dan import Dan_11_0  # noqa: E402

# Import custom generator
try:
    tests_path = os.path.join(os.getcwd(), 'tests')
    if tests_path not in sys.path:
        sys.path.append(tests_path)
    # import garak_probe (removed unused import)
    from garak_probe import VertexAIGenerator
except ImportError as e:
    print(f"Could not import VertexAIGenerator from garak_probe: {e}")
    sys.exit(1)

def load_detector(name):
    try:
        # Check if it has a dot
        if "." in name:
            module_part, class_name = name.rsplit(".", 1)
            full_module_name = f"garak.detectors.{module_part}"
        else:
            # Fallback or assume directly in detectors?
            full_module_name = f"garak.detectors.{name}" # Unlikely
            class_name = name # Unlikely
            
        module = importlib.import_module(full_module_name)
        return getattr(module, class_name)()
    except Exception as e:
        print(f"Error loading detector {name}: {e}")
        raise e

def main():
    print("Initializing Garak Runner...")
    
    # 1. Generator
    # Note: generations=1 for speed in this test
    # The custom generator might print warnings if GCP auth fails
    try:
        generator = VertexAIGenerator(generations=1)
        print("Generator initialized.")
    except Exception as e:
        print(f"Failed to init generator: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 2. Probe
    try:
        probe = Dan_11_0()
        print(f"Probe initialized: {probe.probename}")
    except Exception as e:
        print(f"Failed to init probe: {e}")
        sys.exit(1)

    # 3. Detectors
    detectors = []
    print(f"Recommended detectors: {probe.recommended_detector}")
    for d_name in probe.recommended_detector:
        try:
            d = load_detector(d_name)
            detectors.append(d)
            print(f"Detector loaded: {d_name}")
        except Exception as e:
            print(f"Failed to load detector {d_name}: {e}")

    # 4. Evaluator
    evaluator = None
    print("Evaluator initialized (None).")

    # 5. Run Harness
    h = Harness()
    print("Starting scan...")
    
    # Check if run accepts objects
    try:
        h.run(generator, [probe], detectors, evaluator)
        print("Scan complete.")
    except Exception as e:
        print(f"Scan failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
