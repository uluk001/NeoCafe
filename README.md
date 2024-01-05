# Neocafe

## About

**Neocafe** is an innovative mobile application designed to automate the process of ordering coffee and food in cafes and restaurants. It enables users to place orders quickly and conveniently, track their status in real time, and receive notifications upon order readiness. Neocafe caters to various user roles, including administrators, waiters, and baristas, making it a versatile tool for enhancing service and process management in cafe settings.

## Installation

Ensure your environment is set up with the following:

1. **Python version 3.x**, **redis-server**, and **pip**.
2. Clone the repository:
    ```bash
    git clone https://github.com/uluk001/NeoCafe.git
    ```
3. Navigate to the project directory:
    ```bash
    cd NeoCafe
    ```
4. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
5. Create a `.env` file in the project directory with the following settings (modify as necessary):
    ```bash
    # Cloudinary settings for media files
    CLOUD_NAME=cloudinary
    CLOUD_API_KEY=123456789012345
    CLOUD_API_SECRET=123456789012345

    # Django settings
    DJANGO_SECRET_KEY='secret_key'
    DJANGO_DEBUG='True'

    # Email settings
    EMAIL_HOST='qwerty'
    EMAIL_HOST_USER='apikey'
    EMAIL_HOST_PASSWORD='SG.5Q'
    EMAIL_ADMIN='apikey'

    # Twilio settings
    TWILIO_ACCOUNT_SID='SID'
    TWILIO_AUTH_TOKEN='TOKEN'
    TWILIO_SERVICE_SID='SID'

    # INFOBIP settings
    BASE_URL_INFOBIP="https://api.infobip.com"
    API_KEY_INFOBIP="API_KEY"

    # Database settings
    DB_ENGINE='django.db.backends.sqlite3'
    DB_NAME='db.sqlite3'
    DB_USER='root'
    DB_PASSWORD='root'
    DB_HOST='localhost'
    DB_PORT='3306'

    # Algolia settings
    ALGOLIA_APPLICATION_ID='123456789012345'
    ALGOLIA_API_KEY='123456789012345'

    # Redis settings
    REDIS_HOST='localhost'
    REDIS_PORT='6379'
    ```
6. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
7. Make migrations and migrate:
    ```bash
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```
8. Create a superuser:
    ```bash
    python3 manage.py createsuperuser
    ```
9. Run the app and celery:
    ```bash
    python3 -m uvicorn config.asgi:application --reload
    celery -A config worker -l info
    ```
10. Open the app in your browser at `http://127.0.0.1:8000/swagger/`.

## Technologies and Services

Neocafe utilizes a state-of-the-art technology stack including:

- **Python 3.8**: For backend development, provides high speed development and efficiency.
- **Django REST Framework**: A powerful and flexible framework for building APIs.
- **Redis & Celery**: For asynchronous task processing and data caching.
- **Cloudinary**: Provides convenient media management.
- **Algolia**: Enables advanced search capabilities.
- **Twilio & Infobip**: Facilitate SMS and voice communications.

## Roles

- **User**: Can register, view menus, place orders, track their status and receive notifications.
- **Administrator**: Manages branches, menus, employees and orders.
- **Waiter/Barista**: Processes and fulfills orders.

## Using the API

The Neocafe backend provides a RESTful API for managing coffee and food orders, user accounts, and more. Below is a guide on how to start interacting with our API endpoints.

### API Overview

Our API allows you to programmatically perform actions like creating new orders, updating user profiles, and more. The API is organized around REST. Our API has predictable resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.

### Authentication

Our API uses API keys to authenticate requests. You can view and manage your API keys in the Dashboard. Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.

### API Endpoints

[List of API endpoints and their descriptions]

## Contributing

We welcome contributions to the Neocafe project! If you're interested in helping improve Neocafe, please follow these steps:

1. **Fork the repository**: This creates your own copy of the repository where you can make your changes.
2. **Create a new branch**: Use the command `git checkout -b feature/AmazingFeature` to create a new branch for your feature.
3. **Make your changes**: Implement your new feature or bug fix in this branch.
4. **Commit your changes**: Use the command `git commit -m 'Add some AmazingFeature'` to save your changes with a descriptive commit message.
5. **Push the branch**: Use the command `git push origin feature/AmazingFeature` to upload your changes to your forked repository.
6. **Open a Pull Request**: Go to the GitHub page of your forked repository and click on "New pull request" to submit your changes for review.

## Author & Contact

- **Ismailov** - Initial work - [uluk001](https://github.com/uluk001)

If you have questions, suggestions, or would like to report a bug, feel free to contact me at [ulukmanmuratov@gmail.com](mailto:ulukmanmuratov@gmail.com), via Telegram [@ismailovvv001](https://t.me/ismailovvv001), or connect with me on [LinkedIn](https://www.linkedin.com/in/ismailov-uluk-92784a233/).
