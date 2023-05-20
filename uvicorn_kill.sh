kill -9 $(pgrep -f "uvicorn" | head -n 1)
kill $(lsof -t -i:8000)