# EXIF-based Photo Renaming

This document explains the EXIF-based photo renaming functionality and the standalone script provided in this repository.

## Overview

The `rename_photos_exif.py` script allows you to automatically rename photos based on their EXIF metadata. This provides a more consistent and informative naming scheme for your photo collection without moving files from their original locations.

## Renaming Rules

The script uses two different naming patterns:

1. **Photos with EXIF Data**: Renamed using camera make, model, and date/time information
2. **Photos without EXIF Data**: Renamed using parent folder name, creation date, and original filename

### Naming Pattern for Photos with EXIF Data

Photos with valid EXIF metadata are renamed using this pattern:
```
{Make}_{Model}_{YYYY-MM-DD}_{HH-MM-SS}.{extension}
```

For example:
- `IMG_1234.jpg` → `Canon_EOS90D_2024-03-24_15-30-45.jpg`
- `DSC00123.jpg` → `Sony_A7III_2024-03-24_15-30-45.jpg`

This naming scheme provides immediate information about:
- What camera took the photo (make and model)
- When the photo was taken (date and time)

### Naming Pattern for Photos without EXIF Data

For photos that don't have EXIF metadata (or have incomplete EXIF data), the script uses this pattern:
```
{parent_dir}_{YYYY-MM-DD}_{original-filename}.{extension}
```

For example:
- `IMG_1234.jpg` in a folder named "Vacation" → `Vacation_2024-03-24_IMG_1234.jpg`

This approach:
- Uses the parent folder name as context (often indicating the event or location)
- Adds the file creation date for chronological reference
- Preserves the original filename to maintain any existing organization

## Supported Image Formats

The script works with various image formats:
- JPEG (jpg, jpeg, jfif)
- PNG
- TIFF (tif, tiff)
- RAW formats (arw, nef, cr2, dng, raw)
- HEIC (High Efficiency Image Format)

## Standalone Script Usage

The `rename_photos_exif.py` script can be used independently of the organize-tool:

```bash
# Basic usage (current directory)
python rename_photos_exif.py .

# Specify a directory
python rename_photos_exif.py /path/to/photos

# Simulation mode (no actual changes)
python rename_photos_exif.py /path/to/photos --simulate

# Process subdirectories
python rename_photos_exif.py /path/to/photos --recursive

# Verbose output
python rename_photos_exif.py /path/to/photos --verbose
```

### Command Line Options

- `source_dir`: Directory containing photos to rename (required)
- `--simulate`, `-s`: Run in simulation mode without making actual changes
- `--recursive`, `-r`: Process subdirectories
- `--verbose`, `-v`: Show detailed output
- `--help`, `-h`: Show help message
- `--version`: Show version information

## How It Works

1. The script identifies image files by their extensions
2. It checks if each file contains EXIF metadata
3. For files with EXIF data, it extracts the camera make, model, and date/time information
4. For files without EXIF data, it uses the parent directory name and file creation date
5. Files are renamed according to the appropriate pattern
6. A summary is displayed showing how many files were processed, renamed, or skipped

## Benefits

- **Consistent Naming**: All photos follow a standardized naming convention
- **Self-Documenting**: Filenames contain useful metadata about the photos
- **Improved Searchability**: Easier to find photos by camera type or date
- **Context Preservation**: For photos without EXIF data, the parent folder name provides context
- **Chronological Sorting**: Files naturally sort in chronological order when sorted alphabetically
- **Non-Destructive**: Simulation mode allows previewing changes before applying them
- **Flexible**: Works with or without organize-tool

## Requirements

- Python 3.6 or newer
- Pillow library for EXIF extraction (`pip install Pillow`)

## Integration with Organize-Tool

The script can be used alongside organize-tool:

1. First, rename your photos using this script
2. Then, organize them using organize-tool's rules

Alternatively, you can use the EXIF renaming rules in the organize.yaml configuration:

```bash
# Test in simulation mode first (recommended)
./organize-files.sh --simulate

# Run the actual organization
./organize-files.sh --run
```
