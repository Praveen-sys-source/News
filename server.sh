#!/bin/bash
# Server Management Script

case "$1" in
    start)
        echo "Starting server..."
        lsof -ti:8080 | xargs kill -9 2>/dev/null
        nohup python app.py > server.log 2>&1 & echo $! > server.pid
        sleep 2
        if ps -p $(cat server.pid) > /dev/null; then
            echo "✓ Server started (PID: $(cat server.pid))"
            echo "  URL: http://localhost:8080"
        else
            echo "✗ Failed to start server"
            cat server.log
        fi
        ;;
    stop)
        echo "Stopping server..."
        if [ -f server.pid ]; then
            kill $(cat server.pid) 2>/dev/null && echo "✓ Server stopped" || echo "✗ Server not running"
            rm -f server.pid
        else
            echo "✗ No PID file found"
        fi
        ;;
    restart)
        $0 stop
        sleep 1
        $0 start
        ;;
    status)
        if [ -f server.pid ] && ps -p $(cat server.pid) > /dev/null; then
            echo "✓ Server is running (PID: $(cat server.pid))"
            echo ""
            curl -s -o /dev/null -w "Home: %{http_code}\n" http://localhost:8080/
            curl -s -o /dev/null -w "CSS: %{http_code}\n" http://localhost:8080/static/css/style.css
            curl -s -o /dev/null -w "JS: %{http_code}\n" http://localhost:8080/static/js/main.js
        else
            echo "✗ Server is not running"
        fi
        ;;
    logs)
        tail -f server.log
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        exit 1
        ;;
esac
