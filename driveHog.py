from flask import Flask, request, render_template
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import os

app = Flask(__name__)

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Function to authenticate and build the Drive service
def build_drive_service():
    service_account_file = os.getenv('SERVICE_ACCOUNT_FILE')
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    return service

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        folder_link = request.form['folder_link']
        download_path = request.form['path']
        
        # Ensure the directory exists
        os.makedirs(download_path, exist_ok=True)
        
        # Set the environment variable for Google credentials
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('SERVICE_ACCOUNT_FILE')
        
        # Build the Drive service
        drive_service = build_drive_service()
        
        # Extract folder ID from the link
        folder_id = extract_folder_id(folder_link)
        
        # List files in the folder
        files = list_files_in_folder(drive_service, folder_id)
        
        # Download each file in the folder
        for file in files:
            download_file_from_drive(drive_service, file['id'], os.path.join(download_path, file['name']))
        
        return f"Downloaded {len(files)} files from the folder."
    
    except KeyError as e:
        return f"Missing form data: {str(e)}"
    
    except Exception as e:
        return f"Error downloading files: {str(e)}"

def extract_folder_id(folder_link):
    # Extract folder ID from shared link if needed (e.g., extract from URL)
    # Example: https://drive.google.com/drive/folders/FOLDER_ID
    folder_id = folder_link.split('/')[-1]
    return folder_id

def list_files_in_folder(drive_service, folder_id):
    results = drive_service.files().list(q=f"'{folder_id}' in parents",
                                         pageSize=1000).execute()
    items = results.get('files', [])
    return items

def download_file_from_drive(drive_service, file_id, output_path):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(output_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

