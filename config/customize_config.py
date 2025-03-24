#!/usr/bin/env python3
"""
customize_config.py - Script to customize the organize-tool configuration

This script allows you to easily update the source and destination directories
in the organize-tool configuration file without having to manually edit the YAML file.
It can be run with command-line arguments or in interactive mode.
"""

import os
import sys
import yaml
import argparse
import re
from pathlib import Path
from collections import defaultdict


def load_config(config_path):
    """Load the YAML configuration file."""
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading configuration file: {e}")
        sys.exit(1)


def save_config(config, config_path):
    """Save the configuration to the YAML file."""
    try:
        with open(config_path, 'w') as file:
            yaml.dump(config, file, default_flow_style=False, sort_keys=False)
        print(f"Configuration saved to {config_path}")
    except Exception as e:
        print(f"Error saving configuration file: {e}")
        sys.exit(1)


def update_source_directories(config, source_dir):
    """Update all source directories in the configuration to a static value."""
    count = 0
    for rule in config.get('rules', []):
        if 'locations' in rule:
            # Convert to list if it's not already
            if not isinstance(rule['locations'], list):
                rule['locations'] = [rule['locations']]
            
            # Replace all locations with the new source directory
            for i, location in enumerate(rule['locations']):
                if isinstance(location, dict) and 'path' in location:
                    rule['locations'][i]['path'] = source_dir
                    count += 1
                elif isinstance(location, str):
                    rule['locations'][i] = source_dir
                    count += 1
    
    print(f"Updated {count} source directory references to: {source_dir}")
    return config


def update_destination_base(config, dest_base):
    """Update all destination directories to use the new base path while preserving the folder structure."""
    count = 0
    
    # Normalize dest_base to remove trailing slash
    dest_base = dest_base.rstrip('/')
    
    # Define the standard folder structure based on the user's specification
    organized_paths = {
        'Documents/Text/': f"{dest_base}/Organized/Documents/Text/",
        'Documents/Office/': f"{dest_base}/Organized/Documents/Office/",
        'Documents/PDF/': f"{dest_base}/Organized/Documents/PDF/",
        'Documents/Other/': f"{dest_base}/Organized/Documents/Other/",
        'Media/Images/Photos/': f"{dest_base}/Organized/Media/Images/Photos/",
        'Media/Images/Raw/': f"{dest_base}/Organized/Media/Images/Raw/",
        'Media/Images/Vector/': f"{dest_base}/Organized/Media/Images/Vector/",
        'Media/Images/Adobe/': f"{dest_base}/Organized/Media/Images/Adobe/",
        'Media/Audio/': f"{dest_base}/Organized/Media/Audio/",
        'Media/Audio/Playlists/': f"{dest_base}/Organized/Media/Audio/Playlists/",
        'Media/Video/': f"{dest_base}/Organized/Media/Video/",
        'Development/Code/': f"{dest_base}/Organized/Development/Code/",
        'Development/Web/': f"{dest_base}/Organized/Development/Web/",
        'Development/Data/': f"{dest_base}/Organized/Development/Data/",
        'Development/Data/Database/': f"{dest_base}/Organized/Development/Data/Database/",
        'Archives/': f"{dest_base}/Organized/Archives/",
        'Archives/Split/': f"{dest_base}/Organized/Archives/Split/",
        'Applications/': f"{dest_base}/Organized/Applications/",
        'Fonts/': f"{dest_base}/Organized/Fonts/",
        'System/Config/': f"{dest_base}/Organized/System/Config/",
        'Other/': f"{dest_base}/Organized/Other/",
        'Other/NoExtension/': f"{dest_base}/Organized/Other/NoExtension/",
        'Cleanup/Temporary/': f"{dest_base}/Cleanup/Temporary/",
        'Cleanup/Logs/': f"{dest_base}/Cleanup/Logs/",
        'Cleanup/System/': f"{dest_base}/Cleanup/System/",
        'Cleanup/ErrorReports/': f"{dest_base}/Cleanup/ErrorReports/",
        'Cleanup/Duplicates/': f"{dest_base}/Cleanup/Duplicates/",
        'Cleanup/Duplicates/Music/': f"{dest_base}/Cleanup/Duplicates/Music/",
        'Cleanup/Duplicates/Images/': f"{dest_base}/Cleanup/Duplicates/Images/",
        'Cleanup/Duplicates/Videos/': f"{dest_base}/Cleanup/Duplicates/Videos/",
        'Cleanup/Duplicates/Other/': f"{dest_base}/Cleanup/Duplicates/Other/",
        'Cleanup/URLFragments/': f"{dest_base}/Cleanup/URLFragments/",
        'Cleanup/Unknown/': f"{dest_base}/Cleanup/Unknown/",
    }
    
    # Add additional mappings for common path patterns
    additional_mappings = {
        # Add mappings for paths with just the category name
        'Organized': f"{dest_base}/Organized",
        'Cleanup': f"{dest_base}/Cleanup",
        # Add mappings for paths with /Organized/ or /Cleanup/
        '/Organized/': f"{dest_base}/Organized/",
        '/Cleanup/': f"{dest_base}/Cleanup/",
    }
    organized_paths.update(additional_mappings)
    
    for rule in config.get('rules', []):
        if 'actions' in rule:
            for action in rule['actions']:
                if isinstance(action, dict) and 'move' in action:
                    if isinstance(action['move'], dict) and 'dest' in action['move']:
                        old_dest = action['move']['dest']
                        
                        # Extract the relative path pattern
                        new_dest = update_path(old_dest, dest_base, organized_paths)
                        if new_dest != old_dest:
                            action['move']['dest'] = new_dest
                            count += 1
                    
                    elif isinstance(action['move'], str):
                        old_dest = action['move']
                        
                        # Extract the relative path pattern
                        new_dest = update_path(old_dest, dest_base, organized_paths)
                        if new_dest != old_dest:
                            action['move'] = new_dest
                            count += 1
    
    print(f"Updated {count} destination directory references to use base: {dest_base}")
    return config


def update_path(old_path, dest_base, organized_paths):
    """Update a path to use the new destination base while preserving folder structure."""
    # Handle paths with placeholders like {extension}
    if '{' in old_path and '}' in old_path:
        # Find the most appropriate match in organized_paths
        best_match = None
        best_match_len = 0
        
        for pattern_key, full_path in organized_paths.items():
            # Check if this pattern is a good match for our path
            # We look for the pattern without placeholders
            pattern_parts = pattern_key.split('{')[0].strip('/')
            if pattern_parts and pattern_parts in old_path.split('{')[0]:
                if len(pattern_parts) > best_match_len:
                    best_match = pattern_key
                    best_match_len = len(pattern_parts)
        
        if best_match:
            # Extract the placeholder part
            placeholder_part = old_path.split('/')[-1] if '/' in old_path else old_path
            if not '{' in placeholder_part:  # No placeholder in the last part
                base_path = organized_paths[best_match]
                return base_path
            else:
                # Get the base path without the file part
                base_path = '/'.join(organized_paths[best_match].split('/')[:-1])
                return f"{base_path}/{placeholder_part}"
        
        # If no good match, just replace the base
        path_parts = old_path.split('/')
        rel_path_start = 0
        
        # Find where the actual relative path starts
        for i, part in enumerate(path_parts):
            if part.startswith('{') or 'Organized' in part or 'Cleanup' in part:
                rel_path_start = i
                break
        
        rel_path = '/'.join(path_parts[rel_path_start:])
        return f"{dest_base}/{rel_path}"
    else:
        # Handle direct paths without placeholders
        # First try exact matches
        for pattern_key, full_path in organized_paths.items():
            if pattern_key.strip('/') in old_path:
                # Match found, replace with the new full path
                return full_path
        
        # If no exact match, try to match based on path components
        old_path_lower = old_path.lower()
        for pattern_key, full_path in organized_paths.items():
            pattern_parts = pattern_key.lower().split('/')
            for part in pattern_parts:
                if part and part in old_path_lower:
                    # Found a matching component, extract the relative path
                    path_parts = old_path.split('/')
                    
                    # Find the index of the matching part
                    match_idx = -1
                    for i, p in enumerate(path_parts):
                        if part.lower() in p.lower():
                            match_idx = i
                            break
                    
                    if match_idx >= 0:
                        # Extract the relative path from the matching part onwards
                        rel_path = '/'.join(path_parts[match_idx:])
                        # Replace the pattern key part with the full path
                        return full_path
        
        # If still no match, handle as general case
        path_parts = old_path.split('/')
        
        # Find where the actual relative path starts after home or base dir
        rel_path_start = 0
        for i, part in enumerate(path_parts):
            if part.lower() in ('organized', 'cleanup', 'documents', 'media', 'development', 
                               'archives', 'applications', 'fonts', 'system', 'other'):
                rel_path_start = i
                break
        
        # Build the new path with the destination base
        if rel_path_start > 0:
            rel_path = '/'.join(path_parts[rel_path_start:])
            # Check if this is a Cleanup path
            if path_parts[rel_path_start].lower() == 'cleanup' or any(cleanup_term in rel_path.lower() 
                                                                     for cleanup_term in ['duplicates', 'temporary', 'logs', 'unknown']):
                return f"{dest_base}/{rel_path}"
            else:
                # Default to Organized path
                return f"{dest_base}/{rel_path}"
        else:
            # Fallback - determine if this is likely a Cleanup or Organized path
            path_lower = old_path.lower()
            if any(cleanup_term in path_lower for cleanup_term in ['cleanup', 'duplicates', 'temporary', 'logs', 'unknown']):
                # This looks like a Cleanup path
                return f"{dest_base}/Cleanup/{os.path.basename(old_path)}"
            else:
                # Default to Organized/Other
                return f"{dest_base}/Organized/Other/{os.path.basename(old_path)}"


def find_base_directory(paths):
    """Find the base directory (before Organized/Cleanup) from a list of paths."""
    if not paths:
        return ""
    
    # First, try to extract the base directory directly from the paths
    # Most paths will be in the format: /base/dir/Organized/... or /base/dir/Cleanup/...
    base_candidates = []
    
    for path in paths:
        # Look for /Organized/ or /Cleanup/ in the path
        organized_match = re.search(r'(.+?)/(Organized|Cleanup)/', path, re.IGNORECASE)
        if organized_match:
            base_dir = organized_match.group(1)
            base_candidates.append(base_dir)
    
    # If we found base candidates, use the most common one
    if base_candidates:
        # Count occurrences of each base directory
        base_counts = {}
        for base in base_candidates:
            base_counts[base] = base_counts.get(base, 0) + 1
        
        # Return the most common base directory
        most_common_base = max(base_counts.items(), key=lambda x: x[1])[0]
        return most_common_base
    
    # Fallback: find the longest common prefix
    path_components = [p.split('/') for p in paths]
    min_path_len = min(len(components) for components in path_components)
    
    common_prefix = []
    for i in range(min_path_len):
        current = path_components[0][i]
        if all(p[i] == current for p in path_components):
            common_prefix.append(current)
        else:
            break
    
    return '/'.join(common_prefix)


def display_directory_structure(config):
    """Analyze and display the current directory structure in the configuration."""
    # Categories to organize paths
    categories = defaultdict(set)
    all_dest_paths = []
    
    # Extract destination paths from rules
    for rule in config.get('rules', []):
        if 'actions' in rule:
            for action in rule['actions']:
                if isinstance(action, dict) and 'move' in action:
                    if isinstance(action['move'], dict) and 'dest' in action['move']:
                        path = action['move']['dest']
                    elif isinstance(action['move'], str):
                        path = action['move']
                    else:
                        continue
                    
                    # Store the path
                    all_dest_paths.append(path)
                    
                    # Categorize the path (case-insensitive matching)
                    path_lower = path.lower()
                    if any(pattern in path_lower for pattern in ['/documents/', 'organized/documents', '/documents']):
                        categories['Documents'].add(path)
                    elif any(pattern in path_lower for pattern in ['/media/', 'organized/media', '/media']):
                        categories['Media'].add(path)
                    elif any(pattern in path_lower for pattern in ['/development/', 'organized/development', '/development']):
                        categories['Development'].add(path)
                    elif any(pattern in path_lower for pattern in ['/archives/', 'organized/archives', '/archives']):
                        categories['Archives'].add(path)
                    elif any(pattern in path_lower for pattern in ['/applications/', 'organized/applications', '/applications']):
                        categories['Applications'].add(path)
                    elif any(pattern in path_lower for pattern in ['/fonts/', 'organized/fonts', '/fonts']):
                        categories['Fonts'].add(path)
                    elif any(pattern in path_lower for pattern in ['/system/', 'organized/system', '/system']):
                        categories['System'].add(path)
                    elif any(pattern in path_lower for pattern in ['/other/', 'organized/other', '/other']):
                        categories['Other'].add(path)
                    elif any(pattern in path_lower for pattern in ['/cleanup/', 'cleanup/', '/duplicates/', 'duplicates/', 
                                                                 '/temporary/', 'temporary/', '/logs/', 'logs/', 
                                                                 '/unknown/', 'unknown/', '/errorreports/', 'errorreports/']):
                        categories['Cleanup'].add(path)
    
    # Find the base directory
    base_dir = find_base_directory(all_dest_paths)
    
    print("\nDirectory Structure Analysis:")
    print(f"Base directory: {base_dir}")
    print("\nCategory breakdown:")
    
    # Display categories with example paths
    for category, paths in categories.items():
        print(f"\n{category} ({len(paths)} paths):")
        # Show up to 3 examples per category
        for i, path in enumerate(sorted(list(paths))):
            if i < 3:
                # Show the path relative to the base directory
                rel_path = path
                if base_dir and path.startswith(base_dir):
                    rel_path = path[len(base_dir):].lstrip('/')
                print(f"  - {rel_path}")
            else:
                print(f"  - ... ({len(paths) - 3} more)")
                break
    
    # Count destination categories for summary (case-insensitive)
    dest_categories = {
        'Organized': sum(1 for p in all_dest_paths if 'organized/' in p.lower() or 
                         any(x.lower() in p.lower() for x in ['/documents/', '/media/', '/development/', 
                                                            '/archives/', '/applications/', '/fonts/', 
                                                            '/system/', '/other/'])),
        'Cleanup': sum(1 for p in all_dest_paths if 'cleanup/' in p.lower() or 
                       any(x.lower() in p.lower() for x in ['/cleanup/', '/duplicates/', '/temporary/', 
                                                          '/logs/', '/urlfragments/', '/unknown/', 
                                                          '/errorreports/']))
    }
    
    print("\nDestination Summary:")
    print(f"  - Organized paths: {dest_categories['Organized']}")
    print(f"  - Cleanup paths: {dest_categories['Cleanup']}")
    print(f"  - Total paths: {len(all_dest_paths)}")


def interactive_mode():
    """Run the script in interactive mode, prompting the user for input."""
    print("\n=== Organize-Tool Configuration Customization ===")
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ask for config file location
    default_config = os.path.join(script_dir, 'organize.yaml')
    config_path = input(f"Path to configuration file [default: {default_config}]: ").strip()
    if not config_path:
        config_path = default_config
    
    # Resolve the config path
    if not os.path.isabs(config_path):
        config_path = os.path.join(script_dir, config_path)
    
    # Check if config file exists
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found at {config_path}")
        create_new = input("Would you like to create a new configuration file? (y/n): ").lower()
        if create_new == 'y':
            # Create a minimal default config
            default_config = {
                'rules': [
                    {
                        'locations': ['~/Downloads'],
                        'actions': [
                            {'move': '~/Organized'}
                        ]
                    }
                ]
            }
            save_config(default_config, config_path)
            config = default_config
        else:
            print("Exiting. Please provide a valid configuration file path.")
            sys.exit(1)
    else:
        # Load the configuration
        config = load_config(config_path)
    
    # Show current configuration
    print("\n=== Current Configuration ===")
    display_directory_structure(config)
    
    # Ask for source directory
    update_source = input("\nDo you want to update source directories? (y/n): ").lower()
    if update_source == 'y':
        source_dir = input("Enter new source directory path: ").strip()
        source_dir = os.path.expanduser(source_dir)
        config = update_source_directories(config, source_dir)
    
    # Ask for destination base
    update_dest = input("\nDo you want to update destination directories? (y/n): ").lower()
    if update_dest == 'y':
        dest_base = input("Enter new destination base directory path: ").strip()
        dest_base = os.path.expanduser(dest_base)
        config = update_destination_base(config, dest_base)
    
    # Save the updated configuration
    if update_source == 'y' or update_dest == 'y':
        save_config(config, config_path)
        print("Configuration updated successfully.")
    else:
        print("No changes were made to the configuration.")


def main():
    """Main function to parse arguments and update the configuration."""
    parser = argparse.ArgumentParser(description='Customize organize-tool configuration')
    parser.add_argument('--config', '-c', default='organize.yaml',
                        help='Path to the configuration file (default: organize.yaml)')
    parser.add_argument('--source', '-s', 
                        help='Source directory to scan for files')
    parser.add_argument('--dest-base', '-d',
                        help='Base destination directory for organized files')
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Run in interactive mode')
    parser.add_argument('--check', action='store_true',
                        help='Check the current configuration without making changes')
    
    args = parser.parse_args()
    
    # Check if interactive mode is requested
    if args.interactive:
        interactive_mode()
        return
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Resolve the config path
    if not os.path.isabs(args.config):
        config_path = os.path.join(script_dir, args.config)
    else:
        config_path = args.config
    
    # Load the configuration
    config = load_config(config_path)
    
    # Check mode - just display current configuration
    if args.check:
        print("\nCurrent Configuration:")
        
        # Find representative source directories
        source_examples = set()
        for rule in config.get('rules', []):
            if 'locations' in rule:
                if isinstance(rule['locations'], list):
                    for loc in rule['locations']:
                        if isinstance(loc, dict) and 'path' in loc:
                            source_examples.add(loc['path'])
                        elif isinstance(loc, str):
                            source_examples.add(loc)
                elif isinstance(rule['locations'], str):
                    source_examples.add(rule['locations'])
        
        if source_examples:
            print(f"Source directories: {', '.join(source_examples)}")
        
        # Display complete directory structure
        display_directory_structure(config)
        
        return
    
    # Update source directories if specified
    if args.source:
        source_dir = os.path.expanduser(args.source)
        config = update_source_directories(config, source_dir)
    
    # Update destination base if specified
    if args.dest_base:
        dest_base = os.path.expanduser(args.dest_base)
        config = update_destination_base(config, dest_base)
    
    # Save the updated configuration
    if args.source or args.dest_base:
        save_config(config, config_path)
    else:
        print("No changes specified. Use --source or --dest-base to update directories.")
        print("Example: python customize_config.py --source ~/Documents --dest-base ~/Sorted")
        print("Or use --interactive/-i for interactive mode.")
        print("Use --check to view current configuration.")


if __name__ == '__main__':
    main()
