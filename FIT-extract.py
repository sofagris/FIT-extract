# Description: Extracts images from a FIT file in a UEFI firmware update package. # noqa E501
# Author: Roy Michelsen
# Date: 2024-09-28
# Version: 1.0

# The test file is downloaded from Dell's support site:
# https://dl.dell.com/FOLDER11945679M/1/iDRAC-with-Lifecycle-Controller_Firmware_XTFXJ_WN64_7.00.00.173_A00.EXE?uid=86952a18-584b-47f6-f6ac-fa568a55da1b&fn=iDRAC-with-Lifecycle-Controller_Firmware_XTFXJ_WN64_7.00.00.173_A00.EXE # noqa E501

import os
from pyunpack import Archive
import libfdt


def extract_sfx(exe_file_path, output_directory):
    Archive(exe_file_path).extractall(output_directory)
    print(f"Extracting {exe_file_path} completed to {output_directory}")


def extract_images(fit_file_path, output_directory):
    with open(fit_file_path, 'rb') as f:
        fit_data = f.read()

    # Create an FDT object
    fdt = libfdt.Fdt(fit_data)

    # Navigate to the /images node
    images_offset = fdt.path_offset('/images')
    if images_offset < 0:
        print("Could not find the /images node in the FIT file.")
        return

    # Iterating over images
    offset = fdt.first_subnode(images_offset)
    while True:
        if offset < 0:
            break  # No more subnodes

        image_name = fdt.get_name(offset)

        # Checking for image properties
        # Known properties: type, description, data, os, arch,
        # compression, load, entry, hash, signature, size,
        # address, reg, ver, cpio, kernel, layDown, destination
        # ----------------------------------------------------
        # TODO: Investigate how to handle compression.

        # Compression
        if (fdt.hasprop(offset, 'compression')):
            image_compression = fdt.getprop(offset, 'compression')
        else:
            image_compression = "None"

        # Type
        if (fdt.hasprop(offset, 'type')):
            image_type = fdt.getprop(offset, 'type')
        else:
            image_type = "Unknown"

        # Description
        if (fdt.hasprop(offset, 'description')):
            image_desc = fdt.getprop(offset, 'description')
        else:
            image_desc = "Unknown"

        print(f"Processing image: {image_name}, type: {image_type}, Description: {image_desc}, Compression: {image_compression}") # noqa E501

        # Get the data property
        try:
            data = fdt.getprop(offset, 'data')
        except libfdt.FdtException as e:
            if e.err == libfdt.FDT_ERR_NOTFOUND:
                print(f"No data property found for {image_name}")
            else:
                print(f"Error getting data for {image_name}: {e}")
            # Continue to next subnode
        else:
            # Write data to file
            output_file = os.path.join(output_directory, f"{image_name}.bin")
            with open(output_file, 'wb') as img_file:
                img_file.write(data)
            print(f"Extracted {image_name} to {output_file}")

        # Continue to next subnode
        try:
            offset = fdt.next_subnode(offset)
        except libfdt.FdtException as e:
            if e.err == libfdt.FDT_ERR_NOTFOUND:
                # No more subnodes
                break
            else:
                print(f"Error getting next subnode: {e}")
                break


if __name__ == "__main__":
    exe_file = "iDRAC-with-Lifecycle-Controller_Firmware_XTFXJ_WN64_7.00.00.173_A00.EXE" # noqa E501
    output_dir = "firmware"

    extracted_exe_dir = "extracted"
    fit_file = "extracted/payload/firmimgFIT.d9"

    # Create output directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(extracted_exe_dir, exist_ok=True)

    # Extract SFX archive
    extract_sfx(exe_file, extracted_exe_dir)

    # Extract images from FIT file
    extract_images(fit_file, output_dir)
