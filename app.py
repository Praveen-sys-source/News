from app import create_app
import os

if __name__ == '__main__':
    app = create_app()
    cert = os.getenv('SSL_CERT')
    key = os.getenv('SSL_KEY')
    if cert and key:
        app.run(host='0.0.0.0', port=8443, ssl_context=(cert, key), debug=True)
    else:
        app.run(host='0.0.0.0', port=8080, debug=True)
