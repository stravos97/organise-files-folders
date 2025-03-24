# Enhanced Duplicate Handling for Media Files

This document explains the enhanced duplicate handling features added to the organize-tool configuration.

## Overview

The configuration has been updated to handle duplicates more intelligently, with specialized rules for different types of media files:

1. **Music Files**: Duplicates are evaluated based on metadata completeness
2. **Image Files**: Duplicates are renamed with "_duplicate_X" suffix
3. **Video Files**: Duplicates are renamed with "_duplicate_X" suffix
4. **Other Files**: Duplicates are renamed with "_duplicate_X" suffix

## Music File Duplicate Handling

For music files, the system evaluates the completeness of metadata tags to determine which file to keep as the original. The file with the most complete metadata is kept as the original, while duplicates are renamed.

### Metadata Evaluation Criteria

The system scores music files based on the presence of these metadata fields:
- Artist (1 point)
- Title (1 point)
- Album (1 point)
- Year/Date (1 point)
- Genre (1 point)
- Cover Art (0.5 points)
- File Size (up to 0.5 points, as a proxy for audio quality)

### Supported Audio Formats

The metadata evaluation works with various audio formats:
- MP3 (ID3 tags)
- FLAC (Vorbis comments)
- AAC/M4A (MP4 tags)
- WAV, OGG, and other formats supported by the mutagen library

## Image and Video Duplicate Handling

For image and video files, the system:
1. Identifies duplicates using byte-by-byte comparison
2. Keeps the oldest file as the original (based on creation date)
3. Renames duplicates with "_duplicate_X" suffix, where X is a counter

## Testing the Metadata Evaluation

A test script is included to demonstrate how the metadata evaluation works:

```bash
# Install required dependencies
pip install mutagen

# Run the test script with two music files
./config/test_music_metadata.py path/to/file1.mp3 path/to/file2.mp3
```

The script will:
1. Evaluate the metadata completeness of both files
2. Display the tags found in each file
3. Show which file would be kept as the original based on metadata completeness

## Requirements

- Python 3.6 or newer
- mutagen library (for music metadata evaluation)
- organize-tool (latest version recommended)

## Usage

Run organize-tool as usual:

```bash
# Test in simulation mode
./organize-files.sh --simulate

# Run the actual organization
./organize-files.sh --run
```

The enhanced duplicate handling will automatically:
1. Keep music files with the most complete metadata
2. Rename duplicates with "_duplicate_X" suffix
3. Organize files according to their types
