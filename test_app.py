#!/usr/bin/env python3
"""Test script to verify the application works correctly"""

from news_app import create_app
import sys

def test_app():
    """Test basic app functionality"""
    print("=" * 60)
    print("Testing News Management System")
    print("=" * 60)
    
    try:
        # Create app
        print("\n1. Creating Flask app...")
        app = create_app()
        print("   ✓ App created successfully")
        
        # Test routes
        print("\n2. Testing routes...")
        with app.test_client() as client:
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
                response = client.get(route)
                status = "✓" if response.status_code == 200 else "✗"
                print(f"   {status} {name}: {response.status_code}")
                if response.status_code != 200:
                    all_passed = False
                    print(f"      Error: {response.data.decode()[:200]}")
        
        if all_passed:
            print("\n" + "=" * 60)
            print("✓ All tests passed! App is working correctly.")
            print("=" * 60)
            return 0
        else:
            print("\n" + "=" * 60)
            print("✗ Some tests failed. Check errors above.")
            print("=" * 60)
            return 1
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(test_app())
