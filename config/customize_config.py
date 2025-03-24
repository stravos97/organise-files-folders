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
from pathlib import Path


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
    """Update all source directories in the configuration."""
    count = 0
    for rule in config.get('rules', []):
        if 'locations' in rule:
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
    """Update all destination directories to use the new base path."""
    count = 0
    for rule in config.get('rules', []):
        if 'actions' in rule:
            for action in rule['actions']:
                if isinstance(action, dict) and 'move' in action:
                    if isinstance(action['move'], dict) and 'dest' in action['move']:
                        # Extract the relative path (after ~/ or the last directory in the path)
                        old_dest = action['move']['dest']
                        if old_dest.startswith('~/'):
                            rel_path = old_dest[2:]  # Remove ~/ prefix
                        else:
                            rel_path = os.path.basename(old_dest)
                        
                        # Create new destination path
                        action['move']['dest'] = os.path.join(dest_base, rel_path)
                        count += 1
                    elif isinstance(action['move'], str):
                        old_dest = action['move']
                        if old_dest.startswith('~/'):
                            rel_path = old_dest[2:]  # Remove ~/ prefix
                        else:
                            rel_path = os.path.basename(old_dest)
                        
                        action['move'] = os.path.join(dest_base, rel_path)
                        count += 1
    
    print(f"Updated {count} destination directory references to use base: {dest_base}")
    return config


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
    
    # Ask for source directory
    update_source = input("Do you want to update source directories? (y/n): ").lower()
    if update_source == 'y':
        source_dir = input("Enter new source directory path: ").strip()
        source_dir = os.path.expanduser(source_dir)
        config = update_source_directories(config, source_dir)
    
    # Ask for destination base
    update_dest = input("Do you want to update destination directories? (y/n): ").lower()
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


if __name__ == '__main__':
    main()