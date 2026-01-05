import boto3
import os
from pathlib import Path
import urllib3
from dotenv import load_dotenv

# Load local .env (for development)
load_dotenv()

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# R2 credentials from environment
R2_ACCOUNT_ID = os.environ.get('R2_ACCOUNT_ID')
R2_ACCESS_KEY_ID = os.environ.get('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY')
BUCKET_NAME = os.environ.get('R2_BUCKET_NAME', 'philharmonia-media')

def upload_to_r2():
    # Initialize S3 client
    s3 = boto3.client(
        's3',
        endpoint_url=f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        verify=False
    )
    
    images_folder = Path('./images')
    all_files = [Path(root)/file for root, dirs, files in os.walk(images_folder) for file in files]
    total_files = len(all_files)
    print(f"📁 Found {total_files} files to upload")
    
    success_count = 0
    fail_count = 0
    
    for i, local_path in enumerate(all_files, 1):
        relative_path = local_path.relative_to(images_folder)
        s3_key = str(relative_path).replace('\\', '/')
        
        print(f'📤 [{i}/{total_files}] Uploading: {s3_key}')
        try:
            s3.upload_file(str(local_path), BUCKET_NAME, s3_key)
            print(f'✅ Success: {s3_key}')
            success_count += 1
        except Exception as e:
            print(f'❌ Failed: {s3_key} - {e}')
            fail_count += 1
    
    print(f"\n🎉 UPLOAD SUMMARY:")
    print(f"✅ Successful: {success_count} files")
    print(f"❌ Failed: {fail_count} files")
    print(f"📊 Total: {total_files} files")

if __name__ == '__main__':
    upload_to_r2()
