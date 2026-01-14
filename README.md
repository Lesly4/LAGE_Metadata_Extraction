# LAGE_Metadata_Extraction


## Metadata Extraction Pipeline

A simple and efficient Python utility for converting laboratory CSV data into structured metadata and consolidated summaries.  
This tool specifically supports **BeadStudio Sample Sheets** and **Thermal Cycler Reports**.

---

## Overview

This utility allows you to convert arbitrary genomic laboratory files into structured JSON and CSV summaries. It is designed to be:

* **Easy to use**: Simple CLI commands for single or batch processing.  
* **Fast**: Efficiently processes entire directories of CSV files.  
* **Flexible**: Supports different extraction logics based on the file type (BeadStudio vs. Thermal).

It includes internal validation logic that logs the status of each processing step. Logged data includes:

* Input and output directory paths  
* Success notifications for batch processing  
* Detailed error handling for "Validity File Errors" or unexpected system issues

---

## Base Execution Structure

The core logic is divided into specialized modules imported by the main controller:

* **Extractor_BeadStudio**: Functions for processing Illumina BeadStudio Sample Sheets  
* **Extractor_Thermal_Report**: Functions for processing Thermal  Report files  

---

## Modules Description

### main.py

Main entry point for command-line execution:

* **Single-file processing**  
* **Batch directory processing**  
* **BeadStudio and Thermal Report  files path**

### Extractor_BeadStudio.py

* **BeadStudio file validation**  
* **Header metadata extraction**  
* **Sample-level data extraction**  
* **ORID and manifest enrichment**  
* **JSON output generation**  
* **Summary CSV creation**

### Extractor_Thermal_Report.py

* **Thermal Report file validation**  
* **Column index-to-name mapping**  
* **Filename-based metadata extraction**  
* **ORID detection**  
* **JSON output generation**  
* **Summary CSV creation**

---
##  Local Setup (Development)

### 1. Clone the repository

```bash
git https://github.com/RitAreaSciencePark/LAGE_Metadata_Extraction.git
cd LAGE_Metadata_Extraction
```

### 2. Create & activate a virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```


### 4. Verify files

Ensure the following files are present in the root directory:

* **main.py**

* **Extractor_BeadStudio.py**

* **Extractor_Thermal_Report.py**

* ....

---
## How to Use the Pipeline

The script accepts file and directory paths as command-line arguments via `argparse`.

### Mode Selection

To choose which processing mode to run, edit the `if __name__ == '__main__':` block at the end of `main.py` to call the desired function.

For example, for **BeadStudio files**:

#### Single File Input

```python
if __name__ == '__main__':
    main_Single_file_BeadStudio()
```
 Run the pipeline:


```bash
python main.py <input_file_dir_path> <csv_file_name> <output_dir_path>
```

Note: *Requires calling **main_Single_file_BeadStudio()** in **main.py**.*


**Batch Directory Input**

```python
if __name__ == '__main__':
    main_Multi_file_BeadStudio()    
```

Run the pipeline:

```bash
python main.py <input_dir_path> <output_dir_path>
```

Note: *Requires calling **main_Multi_file_BeadStudio()** in **main.py**.*

