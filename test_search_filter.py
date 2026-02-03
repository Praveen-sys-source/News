#!/usr/bin/env python3
"""
Test search and filter functionality
"""
from news_app import create_app
from news_app.services.article_service import list_articles
from news_app.services.category_service import list_categories

def test_search_filter():
    """Test that search and filter data is available"""
    app = create_app()
    
    with app.test_client() as client:
        # Test articles page
        response = client.get('/articles')
        assert response.status_code == 200
        
        # Test with category filter
        response = client.get('/articles?category=Technology')
        assert response.status_code == 200
        
        # Test with search parameter
        response = client.get('/articles?search=technology')
        assert response.status_code == 200
        
        print("✅ All search and filter routes working")
        
        # Test data availability
        with app.app_context():
            articles = list_articles()
            categories = list_categories()
            
            print(f"✅ {len(articles)} articles available for search")
            print(f"✅ {len(categories)} categories available for filtering")
            
            # Test article data attributes
            if articles:
                article = articles[0]
                print(f"✅ Sample article data:")
                print(f"   Title: {article.title}")
                print(f"   Author: {article.author or 'No author'}")
                print(f"   Category: {article.category.name if article.category else 'No category'}")
                print(f"   Content preview: {article.content[:50]}...")
        
        return True

if __name__ == '__main__':
    try:
        success = test_search_filter()
        if success:
            print("\n🎉 Search and filter functionality test passed!")
        else:
            print("\n❌ Search and filter test failed!")
    except Exception as e:
        print(f"\n❌ Test error: {str(e)}")
        import traceback
        traceback.print_exc()