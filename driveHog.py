import gdown
from google.oauth2 import service_account

# URL of the file in Google Drive
url = 'https://drive.google.com/uc?id=your_file_id'

# Path where you want to save the downloaded file
output = 'downloaded_file.ext'

# Function to download file using service account credentials
def download_file_with_service_account(url, output_path):
    credentials = service_account.Credentials.from_service_account_file(
        'service_account_key.json',
        scopes=['https://www.googleapis.com/auth/drive.readonly']
    )
    
    # Download file using gdown with authenticated credentials
    gdown.download(url, output_path, quiet=False, credentials=credentials)

if __name__ == "__main__":
    download_file_with_service_account(url, output)
