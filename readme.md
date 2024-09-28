# FIT-extract

## Introduction

This project provides tools to extract and analyze data from **Flattened Image Tree (FIT)** files using Python. FIT files are commonly used in embedded systems and firmware updates to package multiple images—such as kernels, device trees, and ramdisks—into a single binary. This project allows you to unpack these files, inspect their contents, and extract individual components for further analysis.

For testing purposes, the **iDRAC with Lifecycle Controller Firmware** executable from Dell was used.

[Download Firmware EXE](https://dl.dell.com/FOLDER11945679M/1/iDRAC-with-Lifecycle-Controller_Firmware_XTFXJ_WN64_7.00.00.173_A00.EXE)

*Note: The download link may become unavailable in the future.*

## Features

- **Extract FIT files** from firmware executables.
- **List the contents** of FIT files in a readable format with syntax highlighting.
- **Extract individual images** from FIT files.
- **Handle SquashFS images** for deeper inspection.

## Installation

### Prerequisites

- **Python 3.x**
- **Required Python packages** listed in `requirements.txt`

### Install Dependencies

To install the necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```

This will install the following packages:

- `libfdt` (Python bindings for libfdt)
- `pyunpack`

## Scripts Overview

### `dump_fit.py`

This script lists the contents of a FIT file in a human-readable format with syntax highlighting. It parses the FIT file structure and displays nodes and properties with colored output for better readability.

#### Usage

```bash
python dump_fit.py [path_to_fit_file]
```

#### Example

```bash
python dump_fit.py extracted/payload/firmimgFIT.d9
```

### `FIT-extract.py`

This script automates the extraction of the firmware executable, locates the FIT file within it, and extracts the individual images contained in the FIT file.

#### Usage

1. **Configure the Script**

   - Ensure the firmware executable (`iDRAC-with-Lifecycle-Controller_Firmware_XTFXJ_WN64_7.00.00.173_A00.EXE`) is in the same directory as the script.
   - Adjust the variables in the script if using a different firmware file:
     ```python
     exe_file = "iDRAC-with-Lifecycle-Controller_Firmware_XTFXJ_WN64_7.00.00.173_A00.EXE"
     extracted_exe_dir = "extracted"
     fit_file = "extracted/payload/firmimgFIT.d9"
     output_dir = "firmware"
     ```

2. **Run the Script**

   ```bash
   python FIT-extract.py
   ```

   The script will:

   - Extract the EXE file into the `extracted` directory.
   - Locate the FIT file (e.g., `extracted/payload/firmimgFIT.d9`).
   - Extract images from the FIT file into the `firmware` directory.

#### Note

- The extracted images may include SquashFS file systems, which can be mounted and explored using appropriate tools.

## Further Usage

### Inspecting SquashFS Images

Many of the extracted files are **SquashFS** images. To mount and investigate them:

1. **Install SquashFS Tools**

   - On Linux:

     ```bash
     sudo apt-get install squashfs-tools
     ```

2. **Mount the SquashFS Image**

   ```bash
   mkdir squashfs-root
   sudo mount -t squashfs -o loop [path_to_squashfs_image] squashfs-root
   ```

3. **Explore the File System**

   Navigate the `squashfs-root` directory to inspect the contents.

### Analyzing Extracted Files

- Use tools like `binwalk`, `hexdump`, or `strings` to analyze binary files.
- Decompile or disassemble firmware binaries for deeper analysis.

## Screenshots

![Screenshot of dump_fit](Screenshot%202024-09-28%20230108.png)

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

### How to Contribute

1. **Fork** the repository.
2. **Create a new branch** for your feature or bugfix.
3. **Commit your changes** with clear commit messages.
4. **Push** your branch to your fork.
5. **Open a pull request** detailing your changes.

## Contact

For any questions or support, please open an issue on the GitHub repository.
