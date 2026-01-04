# download_chinook.py
import urllib.request
import os
from pathlib import Path

def download_chinook_db():
    # Create assets folder if it doesn't exist
    assets_dir = Path(__file__).parent / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    # Download Chinook database
    url = "https://github.com/lerocha/chinook-database/raw/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite"
    db_path = assets_dir / "Chinook.db"
    
    print(f"📁 Assets directory: {assets_dir}")
    print(f"📊 Target database path: {db_path}")
    
    if not db_path.exists():
        print("⬇️ Downloading Chinook database...")
        try:
            # Download the file
            urllib.request.urlretrieve(url, db_path)
            print(f"✅ Successfully downloaded Chinook database!")
            print(f"📁 Location: {db_path}")
            
            # Verify file was downloaded
            if db_path.exists():
                file_size = db_path.stat().st_size
                print(f"📏 File size: {file_size} bytes")
            else:
                print("❌ File download failed")
                
        except Exception as e:
            print(f"❌ Download failed: {e}")
            print("💡 Please check your internet connection")
    else:
        print("✅ Chinook database already exists")
        file_size = db_path.stat().st_size
        print(f"📁 Location: {db_path}")
        print(f"📏 File size: {file_size} bytes")

if __name__ == "__main__":
    print("🚀 Starting Chinook database download...")
    download_chinook_db()
    print("🎉 Download process completed!")

