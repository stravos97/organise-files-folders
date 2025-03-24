# Example Usage of Organize-Tool

This document provides practical examples of how to use the organize-tool with the provided configuration.

## Basic Usage Examples

### Preparing Your Environment

Before running the organization, make sure you have:

1. Installed organize-tool: `pip install -U organize-tool`
2. Customized the configuration for your directories

### Example 1: Organizing Downloads Folder

Let's say you want to organize your Downloads folder:

```bash
# First, customize the configuration to use your Downloads folder
./customize_config.py --source ~/Downloads --dest-base ~/Organized

# Run in simulation mode to see what would happen
./organize-files.sh --simulate

# If the simulation looks good, run the actual organization
./organize-files.sh --run
```

### Example 2: Finding Duplicates in Photos

To find duplicates in your photo collection:

```bash
# First, customize the configuration
./customize_config.py --source ~/Pictures

# Edit the config to enable only the duplicate detection rule
# (You can do this manually or create a custom config file)

# Run in simulation mode
./organize-files.sh --simulate

# Review the results and run if satisfied
./organize-files.sh --run
```

## Advanced Usage Examples

### Example 3: Creating a Custom Configuration for Specific Tasks

You can create custom configurations for specific tasks:

```bash
# Copy the main configuration
cp organize.yaml photos_organize.yaml

# Edit the new configuration to include only photo-related rules
# (You can do this manually)

# Run with the custom configuration
./organize-files.sh --config photos_organize.yaml
```

### Example 4: Scheduled Organization

To set up automatic organization:

1. Create a cron job (Linux/macOS):

```bash
# Edit your crontab
crontab -e

# Add a line to run daily at 2am
0 2 * * * /path/to/organize-files.sh --run
```

2. Or use Task Scheduler on Windows:
   - Create a new task
   - Set the trigger to run daily
   - Set the action to run the script

## Practical Scenarios

### Scenario 1: Post-Download Organization

After downloading files from the internet:

```bash
# Run the organization to sort downloads
./organize-files.sh --run
```

### Scenario 2: Cleaning Up Before Backup

Before backing up your files:

```bash
# First, find and handle duplicates
./organize-files.sh --run

# Then back up the organized files
# (using your preferred backup method)
```

### Scenario 3: Migrating Files to a New Structure

When migrating to a new organization system:

```bash
# Customize the configuration for your source and destination
./customize_config.py --source ~/OldFiles --dest-base ~/NewStructure

# Run in simulation mode
./organize-files.sh --simulate

# Run the actual migration
./organize-files.sh --run
```

## Troubleshooting

If you encounter issues:

1. Check that organize-tool is installed correctly
2. Verify that your configuration file is valid: `organize check --config-file organize.yaml`
3. Run in simulation mode to debug: `./organize-files.sh --simulate`
4. Check the organize-tool documentation: `organize docs`
