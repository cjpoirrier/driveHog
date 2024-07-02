from flask import Flask, request, render_template
import gdown
from google.oauth2 import service_account
import os

app = Flask(__name__)

# Path to your service account credentials JSON file
SERVICE_ACCOUNT_FILE = '/DATA/AppData/gdown/kinetic-physics-391300-7da91d0c1c4c.json'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_path = request.form['path']
    
    # Ensure the directory exists
    os.makedirs(download_path, exist_ok=True)
    
    # Set the environment variable for Google credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_FILE
    
    output = os.path.join(download_path, 'downloaded_file')
    
    # Download file using gdown with service account credentials
    try:
        gdown.download(url, output, quiet=False)
        return f"File downloaded as {output}"
    except Exception as e:
        return f"Error downloading file: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
