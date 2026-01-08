import Extractor

def main():
    """
    Main function to execute the complete metadata extraction pipeline.
    """
    # Define the directory containing CSV files
    directory_path = './Beadstudio_CSVs'
    
    # Define output directory
    output_dir = './Output'
    
    print("=" * 60)
    print("BeadStudio CSV Metadata Extractor")
    print("=" * 60)
    
    # Process all CSV files
    results = Extractor.process_all_csv_files(directory_path, output_dir)
    
    # Create summary table
    summary_table = Extractor.create_summary_table(results)
    
    # Save results
    Extractor.save_results(summary_table, output_dir)
    
    # Display the summary table
    #print("\n" + "=" * 60)
    #print("Metadata Summary Table")
    #print("=" * 60)
    #print(summary_table.to_string(index=False))
    #print("=" * 60)


if __name__ == '__main__':
    main()