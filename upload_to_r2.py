import boto3
import os
from pathlib import Path
import sys

print("=" * 50)
print("📤 CLOUDFLARE R2 FILE UPLOADER")
print("=" * 50)

# Get credentials
R2_ACCOUNT_ID = input("Enter R2 Account ID: ").strip()
R2_ACCESS_KEY_ID = input("Enter R2 Access Key ID: ").strip()
R2_SECRET_ACCESS_KEY = input("Enter R2 Secret Access Key: ").strip()
BUCKET_NAME = 'phil-harmony'

# Validate
if not all([R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY]):
    print("❌ Missing credentials!")
    sys.exit(1)

print(f"\n🔑 Account ID: {R2_ACCOUNT_ID}")
print(f"📦 Bucket: {BUCKET_NAME}")

# Connect to R2
try:
    s3 = boto3.client(
        's3',
        endpoint_url=f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name='auto'
    )
    print("✅ Connected to Cloudflare R2")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    sys.exit(1)

# Check/create bucket
try:
    s3.head_bucket(Bucket=BUCKET_NAME)
    print(f"✅ Bucket exists")
except:
    print(f"⚠️ Creating bucket...")
    try:
        s3.create_bucket(Bucket=BUCKET_NAME)
        print(f"✅ Bucket created")
    except Exception as e:
        print(f"❌ Failed: {e}")
        sys.exit(1)

# Check for images folder
images_folder = Path('./images')
if not images_folder.exists():
    print(f"❌ No 'images' folder found!")
    print("Create an 'images' folder and put files in it")
    sys.exit(1)

# Get all files
all_files = []
for root, dirs, files in os.walk(images_folder):
    for file in files:
        if not file.startswith('.'):  # Skip hidden
            all_files.append(Path(root) / file)

if not all_files:
    print("❌ No files in images folder!")
    sys.exit(1)

print(f"\n📁 Found {len(all_files)} files")

# Upload
success = 0
failed = 0

for i, file_path in enumerate(all_files, 1):
    # Create S3 key
    relative_path = file_path.relative_to(images_folder)
    s3_key = str(relative_path).replace('\\', '/')
    
    print(f"\n[{i}/{len(all_files)}] Uploading: {s3_key}")
    
    try:
        # Upload
        s3.upload_file(
            str(file_path),
            BUCKET_NAME,
            s3_key,
            ExtraArgs={'ACL': 'public-read'}
        )
        
        file_url = f"https://pub-{R2_ACCOUNT_ID[:8]}.r2.dev/{s3_key}"
        print(f"   ✅ Success!")
        print(f"   🔗 {file_url}")
        success += 1
        
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        failed += 1

# Summary
print("\n" + "=" * 50)
print("📊 UPLOAD COMPLETE!")
print("=" * 50)
print(f"✅ Success: {success} files")
print(f"❌ Failed: {failed} files")

if success > 0:
    print(f"\n🌐 Your R2 URL: https://pub-{R2_ACCOUNT_ID[:8]}.r2.dev/")
    print("\n✅ Files are now in Cloudflare R2!")