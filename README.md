# File Organization System

This project provides a comprehensive file organization system using [organize-tool](https://github.com/tfeldmann/organize), a powerful command-line utility for automatically organizing files based on their extensions and other properties.

## Overview

The system is designed to help you organize your files into a structured directory system based on file types. It categorizes files into meaningful groups and handles duplicates, temporary files, and other special cases.

## Features

- **Comprehensive File Organization**: Organizes files based on their extensions into a logical directory structure
- **Duplicate Detection**: Identifies and handles duplicate files
- **Cleanup Rules**: Identifies temporary files, logs, and system files for cleanup
- **Customizable**: Easy to customize source and destination directories
- **Safe Operation**: Includes simulation mode to preview changes before execution

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or install organize-tool directly:
   ```bash
   pip install -U organize-tool
   ```

2. Customize the configuration for your directories:
   ```bash
   cd config
   ./customize_config.py --source ~/YourSourceDir --dest-base ~/YourDestDir
   ```

3. Run in simulation mode to preview changes:
   ```bash
   ./organize-files.sh --simulate
   ```

4. Run the actual organization:
   ```bash
   ./organize-files.sh --run
   ```

## Directory Structure

The system organizes files into the following structure:

```
Organized/
├── Documents/         (txt, pdf, doc, etc.)
├── Media/             (images, audio, video)
├── Development/       (code, web files, databases)
├── Archives/          (zip, rar, etc.)
├── Applications/      (exe, app, etc.)
└── Other/             (other valuable files)

Cleanup/
├── Temporary/         (tmp, bak, etc.)
├── Logs/              (log files)
├── System/            (system files)
└── Duplicates/        (duplicate files)
```

## Documentation

For detailed documentation, see the following files in the `config` directory:

- [README.md](config/README.md): Detailed usage and configuration instructions
- [example_usage.md](config/example_usage.md): Practical examples and scenarios

## Configuration Files

- [organize.yaml](config/organize.yaml): Main configuration file for organize-tool
- [organize-files.sh](config/organize-files.sh): Helper script to run organize-tool
- [customize_config.py](config/customize_config.py): Script to customize the configuration

## License

This project is open source and available under the MIT License.

## Acknowledgements

- [organize-tool](https://github.com/tfeldmann/organize) - The underlying tool that powers this system
