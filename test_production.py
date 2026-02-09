#!/usr/bin/env python3
"""
Production Environment Simulation Test
Tests the app as it would run in production with gunicorn
"""

import subprocess
import time
import requests
import sys
import os

def test_production_server():
    """Test the app with gunicorn"""
    print("=" * 60)
    print("Production Server Test")
    print("=" * 60)
    
    port = 8081  # Use different port to avoid conflicts
    process = None
    
    try:
        # Start gunicorn server
        print(f"\n1. Starting gunicorn server on port {port}...")
        process = subprocess.Popen(
            ['gunicorn', 'app:app', '--bind', f'0.0.0.0:{port}', '--timeout', '30'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd='/workspaces/News'
        )
        
        # Wait for server to start
        print("   Waiting for server to start...")
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print(f"   ✗ Server failed to start")
            print(f"   STDOUT: {stdout.decode()}")
            print(f"   STDERR: {stderr.decode()}")
            return 1
        
        print("   ✓ Server started successfully")
        
        # Test routes
        print("\n2. Testing routes...")
        base_url = f'http://localhost:{port}'
        
        routes_to_test = [
            ('/', 'Home'),
            ('/articles', 'Articles'),
            ('/categories', 'Categories'),
            ('/latest', 'Latest'),
            ('/live-feed', 'Live Feed'),
            ('/static/css/style.css', 'CSS'),
            ('/static/js/main.js', 'JavaScript'),
        ]
        
        all_passed = True
        for route, name in routes_to_test:
            try:
                response = requests.get(f'{base_url}{route}', timeout=5)
                status = "✓" if response.status_code == 200 else "✗"
                print(f"   {status} {name}: {response.status_code}")
                
                if response.status_code != 200:
                    all_passed = False
                    print(f"      Error: {response.text[:200]}")
                    
            except Exception as e:
                print(f"   ✗ {name}: Failed - {e}")
                all_passed = False
        
        print("\n" + "=" * 60)
        if all_passed:
            print("✓ Production server test passed!")
        else:
            print("✗ Some tests failed.")
        print("=" * 60)
        
        return 0 if all_passed else 1
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    finally:
        # Stop the server
        if process:
            print("\n3. Stopping server...")
            process.terminate()
            try:
                process.wait(timeout=5)
                print("   ✓ Server stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                print("   ✓ Server killed")

if __name__ == '__main__':
    # Check if gunicorn is installed
    try:
        import gunicorn
        print("Gunicorn version:", gunicorn.__version__)
    except ImportError:
        print("✗ Gunicorn not installed. Install with: pip install gunicorn")
        sys.exit(1)
    
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("✗ Requests not installed. Install with: pip install requests")
        sys.exit(1)
    
    sys.exit(test_production_server())
