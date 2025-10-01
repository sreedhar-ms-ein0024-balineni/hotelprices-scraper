#!/bin/bash

# Script to create 10 test files, wait 1 minute, then delete them
SCRIPT_DIR="/opt/price-scraper"
LOG_FILE="/opt/price-scraper/test_files_log.txt"

# Log function
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Main script
log_message "Starting test files management"

# Create 10 test files
log_message "Creating 10 test files"
for i in {1..10}; do
    filename="test_file_${i}_$(date +%Y%m%d_%H%M%S).txt"
    echo "This is test file $i created at $(date)" > "${SCRIPT_DIR}/${filename}"
    log_message "Created: $filename"
done

log_message "Waiting 60 seconds before deletion"
sleep 60

# Delete the test files
log_message "Deleting test files"
find "$SCRIPT_DIR" -name "test_file_*_*.txt" -type f -delete
log_message "Test files deletion completed"

log_message "Test files management finished"
