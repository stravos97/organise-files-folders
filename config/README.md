# File Organization System with Organize-Tool

This directory contains a configuration file for organize-tool, a powerful command-line utility for automatically organizing files based on their extensions and other properties.

## Overview

The configuration file (`organize.yaml`) defines rules for organizing files into a structured directory system. It categorizes files based on their extensions and moves them to appropriate directories.

## Directory Structure

The configuration creates the following directory structure:

```
Organized/
├── Documents/
│   ├── Text/          (txt, rtf, md)
│   ├── Office/        (doc, docx, xls, xlsx, ppt, etc.)
│   ├── PDF/           (pdf)
│   └── Other/         (other document formats)
├── Media/
│   ├── Images/
│   │   ├── Photos/    (jpg, jpeg, png, etc.)
│   │   ├── Raw/       (arw, etc.)
│   │   └── Vector/    (svg, ai, eps)
│   ├── Audio/         (mp3, wav, etc.)
│   └── Video/         (mp4, mov, etc.)
├── Development/
│   ├── Code/          (py, js, c, cs, etc.)
│   ├── Web/           (html, css, php, etc.)
│   └── Data/          (json, xml, sql, etc.)
├── Archives/          (zip, rar, 7z, etc.)
├── Applications/      (exe, app, msi, etc.)
├── Fonts/             (ttf, otf, etc.)
├── System/Config/     (ini, cfg, etc.)
└── Other/             (uncategorized but valuable files)

Cleanup/
├── Temporary/         (tmp, bak, etc.)
├── Logs/              (log files)
├── System/            (system-generated files)
├── ErrorReports/      (crash, dmp, etc.)
├── Duplicates/        (duplicate files)
├── URLFragments/      (URL tracking codes)
└── Unknown/           (non-standard entries)
```

## Installation

1. Install organize-tool using pip:

```bash
pip install -U organize-tool
```

2. Ensure you have Python 3.9 or newer installed:

```bash
python --version
```

## Usage

### Using the Helper Script

The included `organize-files.sh` script makes it easy to run organize-tool with the configuration:

```bash
# Run in simulation mode (no actual changes)
./organize-files.sh --simulate

# Run the organization
./organize-files.sh --run

# Use a custom config file
./organize-files.sh --config /path/to/custom-config.yaml

# Show help
./organize-files.sh --help
```

### Manual Usage

You can also run organize-tool directly:

#### Testing the Configuration (Simulation Mode)

Before making any actual changes to your files, test the configuration in simulation mode:

```bash
organize sim --config-file path/to/organize.yaml
```

This will show what would happen without actually moving any files.

#### Running the Configuration

When you're ready to execute the actions:

```bash
organize run --config-file path/to/organize.yaml
```

## Customization

### Using the Customization Script

The included `customize_config.py` script makes it easy to update source and destination directories without manually editing the YAML file:

```bash
# Update source directory
./customize_config.py --source ~/Documents

# Update destination base directory
./customize_config.py --dest-base ~/Sorted

# Update both at once
./customize_config.py --source ~/Documents --dest-base ~/Sorted
```

This script automatically updates all the rules in the configuration file.

### Manual Customization

You can also manually customize the configuration:

1. Open the configuration file:

```bash
organize edit --config-file path/to/organize.yaml
```

2. Replace `~/Downloads` with your source directory in each rule.
3. Modify the destination directories by updating the `dest` parameter in each rule.

### Adding New Rules

To add new rules for specific file types:

1. Copy an existing rule that's similar to what you want to achieve
2. Modify the name, filters, and actions as needed
3. Test the new rule in simulation mode before running it

## Advanced Features

### Duplicate Detection

The configuration includes a rule for finding duplicate files. It compares files byte-by-byte and keeps the oldest file as the original.

### Conflict Handling

When a file with the same name already exists in the destination directory, the configuration uses the `rename_new` strategy, which renames the file being moved by adding a unique suffix.

## Scheduling

You can schedule organize-tool to run automatically using cron (Linux/macOS) or Task Scheduler (Windows).

Example cron entry to run daily at 2am:

```
0 2 * * * /path/to/python -m organize run --config-file /path/to/organize.yaml
```

## Documentation

For more detailed information about organize-tool:

```bash
organize docs
```

This opens the online documentation in your browser.
