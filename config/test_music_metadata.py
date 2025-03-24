#!/usr/bin/env python3
"""
test_music_metadata.py - Script to test the metadata evaluation for music files

This script demonstrates how the metadata evaluation works for music files in the
organize-tool configuration. It takes two music files as input and compares their
metadata completeness using the same logic as in the configuration.
"""

import os
import sys
import argparse
import mutagen

def score_metadata(file_path):
    """
    Score the metadata completeness of a music file.
    Higher score means more complete metadata.
    """
    try:
        audio = mutagen.File(file_path)
        if audio is None:
            print(f"Could not read metadata from {file_path}")
            return 0
        
        score = 0
        tags_found = []
        
        # Check for common tag fields
        # Different audio formats use different tag structures
        # ID3 (MP3)
        if hasattr(audio, 'tags') and audio.tags:
            print(f"File has ID3 tags: {file_path}")
            # ID3 tags
            if 'TPE1' in audio:  # Artist
                score += 1
                tags_found.append("Artist (TPE1)")
            if 'TIT2' in audio:  # Title
                score += 1
                tags_found.append("Title (TIT2)")
            if 'TALB' in audio:  # Album
                score += 1
                tags_found.append("Album (TALB)")
            if 'TDRC' in audio or 'TYER' in audio:  # Year
                score += 1
                tags_found.append("Year (TDRC/TYER)")
            if 'TCON' in audio:  # Genre
                score += 1
                tags_found.append("Genre (TCON)")
            if 'APIC:' in audio or 'APIC' in audio:  # Cover art
                score += 0.5
                tags_found.append("Cover Art (APIC)")
        # FLAC/Vorbis comments
        elif hasattr(audio, 'get'):
            print(f"File has Vorbis comments: {file_path}")
            if audio.get('artist'):
                score += 1
                tags_found.append("Artist")
            if audio.get('title'):
                score += 1
                tags_found.append("Title")
            if audio.get('album'):
                score += 1
                tags_found.append("Album")
            if audio.get('date'):
                score += 1
                tags_found.append("Date")
            if audio.get('genre'):
                score += 1
                tags_found.append("Genre")
            if hasattr(audio, 'pictures') and audio.pictures:
                score += 0.5
                tags_found.append("Cover Art")
        # MP4/AAC
        elif hasattr(audio, 'keys'):
            print(f"File has MP4/AAC tags: {file_path}")
            if '\xa9ART' in audio:  # Artist
                score += 1
                tags_found.append("Artist")
            if '\xa9nam' in audio:  # Title
                score += 1
                tags_found.append("Title")
            if '\xa9alb' in audio:  # Album
                score += 1
                tags_found.append("Album")
            if '\xa9day' in audio:  # Year
                score += 1
                tags_found.append("Year")
            if '\xa9gen' in audio:  # Genre
                score += 1
                tags_found.append("Genre")
            if 'covr' in audio:  # Cover art
                score += 0.5
                tags_found.append("Cover Art")
        
        # Add a small bonus for higher quality files (using file size as a proxy)
        file_size = os.path.getsize(file_path)
        size_score = min(file_size / 10000000, 0.5)  # Max 0.5 points for size
        score += size_score
        
        print(f"File size: {file_size} bytes, Size score: {size_score:.2f}")
        print(f"Tags found: {', '.join(tags_found)}")
        
        return score
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def main():
    parser = argparse.ArgumentParser(description='Compare metadata completeness of music files')
    parser.add_argument('file1', help='First music file')
    parser.add_argument('file2', help='Second music file')
    
    if len(sys.argv) < 3:
        print("Usage: python test_music_metadata.py file1.mp3 file2.mp3")
        sys.exit(1)
    
    args = parser.parse_args()
    
    file1 = args.file1
    file2 = args.file2
    
    if not os.path.exists(file1):
        print(f"Error: File not found: {file1}")
        sys.exit(1)
    
    if not os.path.exists(file2):
        print(f"Error: File not found: {file2}")
        sys.exit(1)
    
    print(f"Evaluating metadata for: {file1}")
    score1 = score_metadata(file1)
    print(f"Metadata score: {score1:.2f}\n")
    
    print(f"Evaluating metadata for: {file2}")
    score2 = score_metadata(file2)
    print(f"Metadata score: {score2:.2f}\n")
    
    print("=== Results ===")
    if score1 > score2:
        print(f"File 1 has better metadata: {file1} (Score: {score1:.2f})")
        print(f"This would be kept as the original.")
        print(f"File 2 would be renamed with _duplicate suffix: {file2} (Score: {score2:.2f})")
    elif score2 > score1:
        print(f"File 2 has better metadata: {file2} (Score: {score2:.2f})")
        print(f"This would be kept as the original.")
        print(f"File 1 would be renamed with _duplicate suffix: {file1} (Score: {score1:.2f})")
    else:
        print(f"Both files have equal metadata scores: {score1:.2f}")
        print("In this case, the first file encountered would be kept as the original.")

if __name__ == '__main__':
    main()
