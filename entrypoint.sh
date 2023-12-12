# Collect static files
python3 manage.py collectstatic --noinput;

# Apply database migrations
python3 manage.py migrate;

# Start server
uvicorn config.asgi:application --host 0.0.0.0 --port 8000;
