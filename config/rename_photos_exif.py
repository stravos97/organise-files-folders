#!/usr/bin/env python3
"""
rename_photos_exif.py - A simple script for renaming photos based on EXIF data

This script renames photos using EXIF metadata when available, or falls back to using
the parent directory name and file creation date when EXIF data is not available.

Usage:
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
"""

import os
import sys
import argparse
import datetime
import re
import logging
from pathlib import Path

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    print("Warning: Pillow library not found. EXIF extraction will be limited.")
    print("Install with: pip install Pillow")

# Constants
VERSION = "1.0.0"
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.heic', '.jfif', '.arw', '.nef', '.cr2', '.dng', '.raw'}

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Rename photos based on EXIF data or parent directory name',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('source_dir', 
                        help='Directory containing photos to rename')
    parser.add_argument('--simulate', '-s', action='store_true',
                        help='Simulation mode - no actual changes')
    parser.add_argument('--recursive', '-r', action='store_true',
                        help='Process subdirectories')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')
    parser.add_argument('--version', action='version', 
                        version=f'%(prog)s {VERSION}')
    
    return parser.parse_args()

def find_image_files(source_dir, recursive=False):
    """Find all image files in the source directory"""
    source_dir = Path(source_dir)
    image_files = []
    
    if recursive:
        # Recursive search
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = Path(root) / file
                if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
                    image_files.append(file_path)
    else:
        # Non-recursive search
        for file in os.listdir(source_dir):
            file_path = source_dir / file
            if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
                image_files.append(file_path)
    
    return image_files

def get_exif_data(img):
    """Extract EXIF data from an image"""
    if not hasattr(img, '_getexif') or img._getexif() is None:
        return None
    
    exif_data = {}
    for tag, value in img._getexif().items():
        decoded = TAGS.get(tag, tag)
        exif_data[decoded] = value
    
    # Process and clean up the data
    processed_data = {}
    
    # Extract make and model
    if 'Make' in exif_data:
        processed_data['make'] = clean_exif_text(exif_data['Make'])
    
    if 'Model' in exif_data:
        processed_data['model'] = clean_exif_text(exif_data['Model'])
    
    # Extract date and time
    if 'DateTimeOriginal' in exif_data:
        try:
            dt = exif_data['DateTimeOriginal']
            # Format: YYYY:MM:DD HH:MM:SS
            if isinstance(dt, str) and len(dt) >= 19:
                date_parts = dt.split(' ')[0].split(':')
                time_parts = dt.split(' ')[1].split(':')
                
                processed_data['datetime'] = {
                    'year': date_parts[0],
                    'month': date_parts[1],
                    'day': date_parts[2],
                    'hour': time_parts[0],
                    'minute': time_parts[1],
                    'second': time_parts[2]
                }
        except Exception as e:
            logger.debug(f"Error processing DateTimeOriginal: {e}")
    
    return processed_data if processed_data else None

def clean_exif_text(text):
    """Clean up text from EXIF data"""
    if not isinstance(text, str):
        return str(text)
    
    # Remove non-printable characters
    text = ''.join(c for c in text if c.isprintable())
    
    # Replace spaces and special characters with underscores
    text = re.sub(r'[^a-zA-Z0-9]', '_', text)
    
    # Remove consecutive underscores
    text = re.sub(r'_+', '_', text)
    
    # Remove leading/trailing underscores
    text = text.strip('_')
    
    return text

def generate_new_filename(file_path, exif_data):
    """Generate a new filename based on EXIF data or fallback pattern"""
    if exif_data and 'make' in exif_data and 'model' in exif_data and 'datetime' in exif_data:
        # Use EXIF data for the filename
        dt = exif_data['datetime']
        make = exif_data['make']
        model = exif_data['model']
        
        # Format: Make_Model_YYYY-MM-DD_HH-MM-SS.ext
        new_filename = f"{make}_{model}_{dt['year']}-{dt['month']}-{dt['day']}_{dt['hour']}-{dt['minute']}-{dt['second']}{file_path.suffix}"
        
        return new_filename
    else:
        # Fallback to parent directory name + creation date + original filename
        try:
            parent_dir = file_path.parent.name
            created = datetime.datetime.fromtimestamp(file_path.stat().st_ctime)
            created_str = created.strftime("%Y-%m-%d")
            
            # Format: ParentDir_YYYY-MM-DD_OriginalName.ext
            new_filename = f"{parent_dir}_{created_str}_{file_path.stem}{file_path.suffix}"
            
            return new_filename
        except Exception as e:
            logger.error(f"Failed to generate fallback filename for {file_path}: {e}")
            return None

def rename_photos(source_dir, simulate=False, recursive=False, verbose=False):
    """Main function to rename photos"""
    # Set logging level based on verbose flag
    if verbose:
        logger.setLevel(logging.DEBUG)
    
    # Check if Pillow is available
    if not PILLOW_AVAILABLE:
        logger.warning("Pillow library not found. EXIF extraction will be limited.")
        logger.warning("Install with: pip install Pillow")
    
    # Find all image files
    image_files = find_image_files(source_dir, recursive)
    
    if not image_files:
        logger.info("No image files found in the specified directory.")
        return
    
    logger.info(f"Found {len(image_files)} image files to process")
    
    # Statistics
    stats = {
        'total_files': len(image_files),
        'renamed_files': 0,
        'skipped_files': 0,
        'error_files': 0,
        'files_with_exif': 0,
        'files_without_exif': 0
    }
    
    # Process each file
    for file_path in image_files:
        try:
            # Extract EXIF data if available
            exif_data = None
            if PILLOW_AVAILABLE:
                try:
                    with Image.open(file_path) as img:
                        exif_data = get_exif_data(img)
                        if exif_data:
                            stats['files_with_exif'] += 1
                            if verbose:
                                logger.debug(f"EXIF data found for {file_path}")
                        else:
                            stats['files_without_exif'] += 1
                            if verbose:
                                logger.debug(f"No EXIF data found for {file_path}")
                except Exception as e:
                    logger.warning(f"Failed to extract EXIF data from {file_path}: {e}")
                    stats['files_without_exif'] += 1
            else:
                stats['files_without_exif'] += 1
            
            # Generate new filename
            new_filename = generate_new_filename(file_path, exif_data)
            if not new_filename:
                logger.warning(f"Could not generate new filename for {file_path}")
                stats['skipped_files'] += 1
                continue
            
            # Check if the new filename is different
            if new_filename == file_path.name:
                logger.info(f"Filename already matches pattern: {file_path}")
                stats['skipped_files'] += 1
                continue
            
            # Create the new path
            new_path = file_path.parent / new_filename
            
            # Handle filename conflicts
            counter = 1
            original_new_path = new_path
            while new_path.exists():
                stem = original_new_path.stem
                suffix = original_new_path.suffix
                new_filename = f"{stem}_{counter}{suffix}"
                new_path = file_path.parent / new_filename
                counter += 1
            
            # Rename the file
            if not simulate:
                try:
                    file_path.rename(new_path)
                    logger.info(f"Renamed: {file_path.name} → {new_filename}")
                    stats['renamed_files'] += 1
                except Exception as e:
                    logger.error(f"Failed to rename {file_path}: {e}")
                    stats['error_files'] += 1
            else:
                logger.info(f"Would rename: {file_path.name} → {new_filename}")
                stats['renamed_files'] += 1
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            stats['error_files'] += 1
    
    # Print summary
    logger.info("\nSummary:")
    logger.info(f"  Total files processed: {stats['total_files']}")
    logger.info(f"  Files with EXIF data: {stats['files_with_exif']}")
    logger.info(f"  Files without EXIF data: {stats['files_without_exif']}")
    logger.info(f"  Files renamed: {stats['renamed_files']}")
    logger.info(f"  Files skipped: {stats['skipped_files']}")
    logger.info(f"  Errors: {stats['error_files']}")
    
    if simulate:
        logger.info("\nThis was a simulation. No files were actually renamed.")
        logger.info("To perform the actual renaming, run without the --simulate flag.")

def main():
    """Main entry point"""
    args = parse_arguments()
    
    try:
        source_dir = Path(args.source_dir)
        if not source_dir.exists() or not source_dir.is_dir():
            logger.error(f"Source directory does not exist: {source_dir}")
            return 1
        
        logger.info(f"Processing directory: {source_dir}")
        logger.info(f"Mode: {'Simulation' if args.simulate else 'Actual'}")
        logger.info(f"Recursive: {'Yes' if args.recursive else 'No'}")
        
        rename_photos(
            source_dir=source_dir,
            simulate=args.simulate,
            recursive=args.recursive,
            verbose=args.verbose
        )
        
        return 0
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
