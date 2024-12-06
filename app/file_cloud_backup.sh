# Get the directory path
DIRECTORY="/app/backups/"

# Check if the directory exists
if [ ! -d "$DIRECTORY" ]; then
  echo "Error: Directory '$DIRECTORY' not found."
  exit 1
fi

# Get the last modified file in the directory
LAST_MODIFIED_FILE=$DIRECTORY$(ls -t "$DIRECTORY" | head -n 1)
echo "$LAST_MODIFIED_FILE"
# Upload the file identified by the file_path variable to File.io cloud
RESPONSE=$(curl -F "file=@$LAST_MODIFIED_FILE" https://file.io)

# Extract the download link from the response
DOWNLOAD_LINK=$(echo $RESPONSE | grep -o '"link":"[^"]*' | grep -o '[^"]*$')

log_file="download_links_backup.txt"

# Print the download link
if [ -n "$DOWNLOAD_LINK" ]; then
  echo "File uploaded successfully. Download link: $DOWNLOAD_LINK"
else
  echo "Failed to upload file."
fi

# Write download link to logs file