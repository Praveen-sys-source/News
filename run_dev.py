#!/usr/bin/env python3
"""Development server startup script"""

from news_app import create_app
import os

if __name__ == '__main__':
    app = create_app()
    
    # Get port from environment or use default
    port = int(os.getenv('PORT', 8080))
    
    print(f"\n{'='*60}")
    print(f"Starting News Management System on port {port}")
    print(f"{'='*60}\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True,
        use_reloader=True
    )
