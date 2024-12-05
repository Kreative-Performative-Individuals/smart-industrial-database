# Get file path from input
FILE_PATH=$1

# Upload the file identified by the file_path variable to File.io cloud
RESPONSE=$(curl -F "file=@$FILE_PATH" https://file.io)

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
echo "$(date): $DOWNLOAD_LINK" >> "$log_file"