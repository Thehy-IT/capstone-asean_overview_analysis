import os
import sys
import subprocess

# Set stdout encoding to utf-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON_PREP_DIR = os.path.join(BASE_DIR, "03_Data_Preprocessing", "Python")

def run_pipeline():
    print("=== STARTING CAPSTONE ASEAN OVERVIEW MASTER PIPELINE ===")
    
    # Step 1: Clean and Transform Raw Datasets into Star Schema
    clean_script = os.path.join(PYTHON_PREP_DIR, "clean_and_transform.py")
    print(f"Step 1: Running Data Cleaning & Transformation ({clean_script})...")
    res1 = subprocess.run([sys.executable, clean_script], check=True)
    
    # Step 2: Generate Jupyter Notebooks
    nb_script = os.path.join(PYTHON_PREP_DIR, "generate_notebooks.py")
    print(f"Step 2: Generating Jupyter Analysis Notebooks ({nb_script})...")
    res2 = subprocess.run([sys.executable, nb_script], check=True)
    
    print("=== MASTER PIPELINE EXECUTED SUCCESSFULLY (EXIT CODE 0) ===")

if __name__ == "__main__":
    run_pipeline()
