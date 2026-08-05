import os
import sys
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "08_Source_Code", "src")

def run_pipeline():
    print("=== STARTING CAPSTONE ASEAN OVERVIEW MASTER PIPELINE ===")
    
    # Step 1: Clean and Transform Raw Datasets into Star Schema
    clean_script = os.path.join(SRC_DIR, "clean_and_transform.py")
    print(f"\nStep 1: Running Data Cleaning & Transformation ({clean_script})...")
    subprocess.run([sys.executable, clean_script], check=True)
    
    # Step 2: Run Automated CI/CD Unit Test Suite
    test_script = os.path.join(SRC_DIR, "test_suite.py")
    print(f"\nStep 2: Running Automated Data Quality Test Suite ({test_script})...")
    subprocess.run([sys.executable, test_script], check=True)

    # Step 3: Generate Jupyter Notebooks
    nb_script = os.path.join(SRC_DIR, "generate_notebooks.py")
    print(f"\nStep 3: Generating Jupyter Analysis Notebooks ({nb_script})...")
    subprocess.run([sys.executable, nb_script], check=True)
    
    print("\n=== MASTER PIPELINE EXECUTED SUCCESSFULLY WITH ALL TESTS PASSED (EXIT CODE 0) ===")

if __name__ == "__main__":
    run_pipeline()
