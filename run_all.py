"""
Master Orchestration Script for White Paper Exposure-Context Analysis
Executes Modules 01 through 10 in sequential order and validates outputs.
"""
import os
import sys
import time

# Ensure workspace root is on sys.path
sys.path.insert(0, os.path.abspath("."))

def run_pipeline():
    start_time = time.time()
    print("======================================================================")
    print("STARTING COMPLETE WHITE PAPER REPRODUCIBLE ANALYSIS PIPELINE")
    print("======================================================================\n")
    
    modules = [
        ("Module 01: Data Coverage Audit", "white_paper.module_01_data_coverage"),
        ("Module 02: Classification and Crosswalk", "white_paper.module_02_classification_and_crosswalk"),
        ("Module 03: Longitudinal Context", "white_paper.module_03_longitudinal_context"),
        ("Module 04: August Matched Comparison", "white_paper.module_04_august_matched_comparison"),
        ("Module 05: Altitude Distribution", "white_paper.module_05_altitude_distribution"),
        ("Module 06: Hourly Overlap and Diurnal Profiles", "white_paper.module_06_hourly_overlap"),
        ("Module 07: Special Categories Analysis", "white_paper.module_07_special_categories"),
        ("Module 08: Publication Figures Generation", "white_paper.module_08_generate_figures"),
        ("Module 09: Trajectory Map Generation", "white_paper.module_09_generate_maps"),
        ("Module 10: Verification Assertions and Manifest", "white_paper.module_10_verification")
    ]
    
    for title, mod_name in modules:
        print(f"\n--- {title} ---")
        mod = __import__(mod_name, fromlist=["run"])
        mod.run()
        
    elapsed = time.time() - start_time
    print("\n======================================================================")
    print(f"PIPELINE COMPLETED SUCCESSFULLY IN {elapsed:.1f} SECONDS")
    print("======================================================================")

if __name__ == "__main__":
    run_pipeline()
