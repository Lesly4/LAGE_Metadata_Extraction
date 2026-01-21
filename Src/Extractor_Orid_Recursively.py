import os
import argparse
import re
import Main_Auto_Processor  # Leverages your established auto-detection logic

# --- 1. UTILITIES ---

def get_orid_from_filename(filename):
    """Extract ORID + first 4 digits from filename."""
    pattern = r"(ORID\d{4})"
    match = re.search(pattern, filename, re.IGNORECASE)
    return match.group(1) if match else None

# --- 2. RECURSIVE CRAWLER LOGIC ---

def process_recursive_by_orid(root_input_dir, target_orid, output_dir):
    """
    Dives into all subdirectories of root_input_dir and processes 
    any CSV matching the target ORID using the Auto-Processor registry.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    width = 90
    print("=" * width)
    print("FILE PROCESSING STARTED".center(width))
    print("=" * width)
    print(f"RECURSIVE SEARCH FOR ORID: {target_orid}")
    print(f"ROOT DIRECTORY: {root_input_dir}")
    print("=" * width)


    successful_count = 0
    total_found_matching = 0

    # os.walk generates the file names in a directory tree
    # It handles 'infinite' nesting by visiting every branch
    for dirpath, dirnames, filenames in os.walk(root_input_dir):
        # Filter for CSV files in the current folder
        csv_files = [f for f in filenames if f.lower().endswith('.csv')]
        
        for file_name in csv_files:
            file_orid = get_orid_from_filename(file_name)
            
            # Check if this file matches our target ORID
            if file_orid and file_orid.upper() == target_orid.upper():
                total_found_matching += 1
                full_path = os.path.join(dirpath, file_name)
                
                print(f"\n🔍 FILE FOUND: {file_name}")
                print(f"   LOCATION: {dirpath}")
                
                # 3. Use your Auto-Detector to identify and process the file
                try:
                    # process_single_path returns a list of results on success
                    result = Main_Auto_Processor.process_single_path(full_path, output_dir)
                    if result:
                        successful_count += 1
                except Exception as e:
                    print(f"   ❌ ERROR processing {file_name}: {e}")

    # --- 3. FINAL SUMMARY ---
    print("\n" + "=" * width)
    print("CRAWL SUMMARY".center(width))
    print("=" * width)
    print(f"Total Matches Found:   {total_found_matching}")
    print(f"Successfully Exported: {successful_count}")
    print(f"Failed/Skipped:        {total_found_matching - successful_count}")
    print(f"Results Directory:     {output_dir}")
    print("=" * width)

# --- 4. COMMAND LINE INTERFACE ---

def main():
    parser = argparse.ArgumentParser(description="Recursively extract data for a specific ORID.")
    parser.add_argument("root_dir", help="The general top-level folder to start the search")
    parser.add_argument("target_orid", help="The ORID to filter for (e.g., ORID0036)")
    parser.add_argument("output_dir", help="Where to save all generated JSON files")

    args = parser.parse_args()
    
    # Normalize ORID input
    target_orid = args.target_orid.strip()
    
    process_recursive_by_orid(args.root_dir, target_orid, args.output_dir)

if __name__ == "__main__":
    main()