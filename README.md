# Neocafe

**Neocafe** is a mobile app for self-call coffee and food ordering. The app allows users to register, browse menus, place orders and track their status, and receive notifications.



## Installation

1. Make sure that you have Python version 3.x installed, redis-server running, and pip installed.
2. Clone the repository from GitHub:
```bash
https://github.com/uluk001/NeoCafe.git
```
3. Go to the project directory:
```bash
cd NeoCafe
```
4. Create a virtual environment:
```bash
python3 -m venv venv
```
5. Activate the virtual environment:
```bash
source venv/bin/activate
```
6. Create a .env file in the project directory and add the following variables:
```bash
# Cloudinary settings for media files
CLOUD_NAME = cloudinary
CLOUD_API_KEY = 123456789012345
CLOUD_API_SECRET = 123456789012345

# Django settings
DJANGO_SECRET_KEY='secret_key'
DJANGO_DEBUG='True'

# Email settings
EMAIL_HOST='qwerty'
EMAIL_HOST_USER='apikey'
EMAIL_HOST_PASSWORD='SG.5Q'
EMAIL_ADMIN='apikey'

# Twilio settings
TWILIO_ACCOUNT_SID = 'SID'
TWILIO_AUTH_TOKEN = 'TOKEN'
TWILIO_SERVICE_SID = 'SID'

# INFOBIP settings
BASE_URL_INFOBIP = "https://api.infobip.com"
API_KEY_INFOBIP = "API_KEY"

# Database settings
DB_ENGINE='django.db.backends.sqlite3' # if you use other database, change this
DB_NAME='db.sqlite3'
DB_USER='root'
DB_PASSWORD='root'
DB_HOST='localhost'
DB_PORT='3306'

# Algolia settings
ALGOLIA_APPLICATION_ID='123456789012345'
ALGOLIA_API_KEY='123456789012345'

# Redis settings
REDIS_HOST='localhost' # if you use other database, change this
REDIS_PORT='6379'
```
7. Install the required packages:
```bash
pip install -r requirements.txt
```
8. Make migrations and migrate:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
9. Create a superuser:
```bash
python3 manage.py createsuperuser
```
10. Run the app and celery:
```bash
python3 -m uvicorn config.asgi:application --reload
celery -A config worker -l info
```
11. Open the app in your browser at http://127.0.0.1:8000/swagger/.



## Technologies and services
- Python 3.8
- Django REST Framework
- Redis
- Celery

### Third-party services
- Cloudinary
- Algolia
- Twilio
- Infobip
