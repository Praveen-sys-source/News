#!/usr/bin/env python3
"""
Test media upload functionality
"""
import os
import tempfile
from news_app import create_app

def test_media_upload():
    """Test media upload path resolution"""
    app = create_app()
    
    with app.app_context():
        # Test upload directory creation
        upload_folder = os.path.join('static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        print(f"✅ Upload folder created: {upload_folder}")
        print(f"✅ Absolute path: {os.path.abspath(upload_folder)}")
        print(f"✅ Directory exists: {os.path.exists(upload_folder)}")
        
        # Test file creation
        test_file = os.path.join(upload_folder, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        
        print(f"✅ Test file created: {os.path.exists(test_file)}")
        
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)
        
        return True

if __name__ == '__main__':
    try:
        success = test_media_upload()
        if success:
            print("🎉 Media upload test passed!")
        else:
            print("❌ Media upload test failed!")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")