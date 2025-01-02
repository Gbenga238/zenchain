#!/bin/bash

# Function to display usage information
usage() {
    echo "Usage: $0 <source_file>"
    echo "Replaces the content of docker-compose.yml with the content of <source_file>"
    exit 1
}

# Check if a source file was provided
if [ $# -ne 1 ]; then
    usage
fi

source_file="$1"

# Check if the source file exists
if [ ! -f "$source_file" ]; then
    echo "Error: Source file '$source_file' not found"
    exit 1
fi

# Create backup of existing docker-compose.yml if it exists
if [ -f "docker-compose.yml" ]; then
    backup_file="docker-compose.yml.backup.$(date +%Y%m%d_%H%M%S)"
    cp docker-compose.yml "$backup_file"
    echo "Created backup: $backup_file"
fi

# Copy the content of the source file to docker-compose.yml
cp "$source_file" docker-compose.yml

# Check if the copy was successful
if [ $? -eq 0 ]; then
    echo "Successfully replaced docker-compose.yml with content from $source_file"
else
    echo "Error: Failed to replace docker-compose.yml"
    # Restore from backup if copy failed and backup exists
    if [ -f "$backup_file" ]; then
        cp "$backup_file" docker-compose.yml
        echo "Restored from backup"
    fi
    exit 1
fi