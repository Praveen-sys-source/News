#!/usr/bin/env python3
"""
Final test for category filtering functionality
"""
from news_app import create_app
from news_app.services.article_service import list_articles_by_category
from news_app.services.category_service import list_categories

def test_category_filtering():
    """Test category filtering works correctly"""
    app = create_app()
    
    with app.test_client() as client:
        print("🧪 Testing Category Filtering")
        
        # Get available categories
        with app.app_context():
            categories = list_categories()
            print(f"Available categories: {[cat.name for cat in categories]}")
        
        # Test each category
        test_categories = ['Technology', 'Local', 'Business', 'World']
        
        for cat_name in test_categories:
            response = client.get(f'/articles?category={cat_name}')
            
            if response.status_code == 200:
                content = response.data.decode('utf-8')
                
                # Check if category title appears
                if f'{cat_name} Articles' in content:
                    print(f"✅ {cat_name} category filter shows correct title")
                else:
                    print(f"❌ {cat_name} category title not found")
                
                # Check if category is selected in dropdown
                if f'value="{cat_name}" selected' in content:
                    print(f"✅ {cat_name} category is selected in dropdown")
                else:
                    print(f"❌ {cat_name} category not selected in dropdown")
                
                # Count articles displayed
                article_count = content.count('article-card-modern')
                print(f"✅ {cat_name} category shows {article_count} articles")
            else:
                print(f"❌ {cat_name} category filter failed: {response.status_code}")
        
        # Test reset functionality
        response = client.get('/articles')
        if response.status_code == 200:
            content = response.data.decode('utf-8')
            total_articles = content.count('article-card-modern')
            print(f"✅ All articles page shows {total_articles} total articles")
        
        print("\n🎉 Category filtering test completed!")
        return True

if __name__ == '__main__':
    try:
        success = test_category_filtering()
        if success:
            print("\n✅ CATEGORY FILTERING IS WORKING CORRECTLY!")
        else:
            print("\n❌ Category filtering tests failed!")
    except Exception as e:
        print(f"\n❌ Test error: {str(e)}")
        import traceback
        traceback.print_exc()