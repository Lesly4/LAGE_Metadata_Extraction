import argparse
import os
import json
import pandas as pd
import re

# Import  extractors modules
import Extractor_BeadStudio
import Extractor_Thermal_Report
import Extractor_FMGeneration
import Extractor_IlluminaSampleSheet
import Extractor_FMAutoTilt

# --- 1. THE REGISTRY ---

# We use a list here because order can matter for auto-detection
EXTRACTORS = [
    Extractor_BeadStudio,
    Extractor_Thermal_Report,
    Extractor_FMGeneration,
    Extractor_IlluminaSampleSheet,
    Extractor_FMAutoTilt
]

# --- 2. THE AUTO-DETECTOR ---

def detect_file_type(file_path):
    """
    Checks the file against every registered extractor's validation logic.
    Returns the module that successfully identifies the file.
    """
    for module in EXTRACTORS:
        # Each module must have an 'is_beadstudio_file' style function
        # We look for the validation function generically
        valid_function_names = [
        'is_beadstudio_file', 
        'is_thermal_report', 
        'is_fm_generation_report', 
        'is_illumina_samplesheet', 
        'is_fm_autotilt_report'
    ]
    
    for module in EXTRACTORS:
        for func_name in valid_function_names:
            validator = getattr(module, func_name, None)
            if validator and validator(file_path):
                return module
    return None

# --- 3. UNIFIED PROCESSING LOGIC ---

def process_single_path(input_path, output_dir):
    """
    Detects the type and processes a single file.
    """
    module = detect_file_type(input_path)
    
    if not module:
        print(f"\n⚠️  Unknown file type detected: {input_path}")
        return None

    # Determine type name from the module name or a variable inside it
    type_label = module.__name__.replace('Extractor_', '')
    print(f"\n📄 File detected ({type_label}): {os.path.basename(input_path)}")

    # Use the standardized 'one_single_file' interface
    input_dir = os.path.dirname(input_path) or "."
    file_name = os.path.basename(input_path)
    
    return module.one_single_file(input_dir, output_dir, file_name)

def main():
    parser = argparse.ArgumentParser(description="Auto-Detecting Metadata Extractor")
    parser.add_argument("input_path", help="Path to a CSV file or directory")
    parser.add_argument("output_dir", help="Where to save results")
    parser.add_argument("--batch", action="store_true", help="Process all files in directory")

    width = 30
    print("=" * width)
    print("FILE PROCESSING STARTED".center(width))
    print("=" * width)


    args = parser.parse_args()
    all_results = []
    total_checked = 0

    if args.batch:
        files = [os.path.join(args.input_path, f) for f in os.listdir(args.input_path) 
                 if f.lower().endswith('.csv')]
        total_checked = len(files)
        for f in files:
            res = process_single_path(f, args.output_dir)
            if res: all_results.extend(res)
    else:
        total_checked = 1
        all_results = process_single_path(args.input_path, args.output_dir) or []

    
    if all_results:
        print("\n" + "=" * width)
        print("Processing Summary".center(width))
        print("=" * width)
        print(f"File(s) Successfully processed: {len(all_results)}")
        print(f"File(s) Skipped / failed:       {total_checked - len(all_results)}")
        print(f"Total files checked:            {total_checked}")
        print("=" * width)

if __name__ == "__main__":
    main()