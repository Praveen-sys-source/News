#!/usr/bin/env python3
"""
Test script to verify deployment setup
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deploy_setup import setup_database

if __name__ == '__main__':
    print("🧪 Testing deployment setup...")
    try:
        success = setup_database()
        if success:
            print("✅ Deployment setup test passed!")
        else:
            print("❌ Deployment setup test failed!")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        sys.exit(1)