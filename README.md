# Neocafe

**Neocafe** is an innovative mobile application designed to automate the process of ordering coffee and food in cafes and restaurants. It allows users not only to make orders quickly and conveniently, but also to track their status in real time, as well as to receive notifications when the order is ready. A special feature of Neocafe is the ability to work with different user roles, including administrators, waiters and baristas, which makes it a versatile tool for improving service and process management in cafes.



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



## Technologies and Services
Neocafe utilizes a state-of-the-art technology stack including:

- **Python 3.8**: For backend development, provides high speed development and efficiency.
- **Django REST Framework**: A powerful and flexible framework for building APIs.
- **Redis & Celery**: For asynchronous task processing and data caching.
- **Cloudinary**: Provides convenient media management.
- **Algolia**: Enables advanced search capabilities.
- **Twilio & Infobip**: Facilitate SMS and voice communications.

Together, these technologies create a powerful platform that can efficiently handle user requests and provide quality service.


## Roles

- **User**: Can register, view menus, place orders, track their status and receive notifications.
- **Administrator**: Manages branches, menus, employees and orders.
- **Waiter/Barista**: Processes and fulfills orders.


## Using the API

The Neocafe backend provides a RESTful API for managing coffee and food orders, user accounts, and more. Below is a guide on how to start interacting with our API endpoints.


**API Overview**:
Our API allows you to programmatically perform actions like creating new orders, updating user profiles, and more. The API is organized around REST. Our API has predictable resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.

**Authentication**:
Our API uses API keys to authenticate requests. You can view and manage your API keys in the Dashboard. Your API keys carry many privileges, so be sure to keep them secure! Do not share your secret API keys in publicly accessible areas such as GitHub, client-side code, and so forth.


### API Endpoints
**Accounts**
- `/accounts/` - Various operations related to account management, including registering, logging in, editing profile and setting birthdate.
- `/accounts/admin-login/` - Login for administrator.
- `/accounts/confirm-login/` and `/accounts/confirm-phone-number/` - Login and phone number confirmation.
- `/accounts/login-for-client/`, `/accounts/login-waiter/`, `/accounts/login/`, `/accounts/temporary-login-waiter/` and `/accounts/temporary-login/` - Different login methods for customers and waiters.
- `/accounts/my-profile/` and `/accounts/my-schedule/` - Retrieve a user's profile and schedule.
- `/accounts/refresh/` - Refreshing a session.
- `/accounts/resend-code-with-pre-token/` and `/accounts/resend-code/` - Resend confirmation code.
- `/accounts/update-waiter-profile/` - Update waiter profile.

**Admin Panel**
- `/admin-panel/categories/` - Category management (receiving, creating, deleting, updating).
- `/admin-panel/employees/` - Manage employees (retrieve, create, delete, update, schedule management).
- `/admin-panel/ingredient-destroy-from-branch/{id}/` and `/admin-panel/ingredient-quantity-in-branch/{id}/` - Manage ingredients on branch (delete, retrieve, update).
- `/admin-panel/ingredients/` - Manage ingredients (receive, create, delete, update).
- `/admin-panel/items/` - Manage items (retrieve, create, delete, update, add image).
- `/admin-panel/low-stock-ingredient-branch/{id}/` - Receive low-stock ingredients on a branch.
- `/admin-panel/ready-made-products/` - Manage ready-made products (receive, create, delete, update, add image, update quantity).

**Branches**
- `/branches/` - Receive and create branches.
- `/branches/delete/{id}/` and `/branches/update/{id}/` - Deleting and updating a branch.
- `/branches/image/{id}/` - Adding and updating a branch image.
- `/branches/schedule/update/{id}/` - Updating a branch's schedule.

**Customers**
- `/customers/branches/` and `/customers/categories/` - Retrieve branches and categories.
- `/customers/change-branch/` and `/customers/check-if-item-can-be-made/` - Change a branch and check if an item can be made.
- `/customers/compatible-items/{item_id}/` and `/customers/menu/{item_id}/` - Retrieve compatible items and a detailed list of menu items.
- `/customers/my-bonus/`, `/customers/my-id/`, `/customers/my-orders/` - Retrieve user's bonuses, id and orders.
- `/customers/popular-items/` - Getting popular items.

**Notices**
- `/notices/clear-admin-notifications/`, `/notices/clear-waiter-notifications/` - Clearing administrator and waiter notifications.
- `/notices/delete-admin-notification/`, `/notices/delete-barista-notification/`, `/notices/delete-client-notification/`, `/notices/delete-reminder/` - Deleting administrator, barista, customer notifications and reminders.

**Ordering**
- `/ordering/add-item-to-order/`, `/ordering/create-order/`, `/ordering/remove-order-item/` - Adding an item to an order, creating an order, removing an item from an order.
- `/ordering/reorder-information/`, `/ordering/reorder/` - Retrieve reorder information and reorder.

**Waiter**
- `/waiter/get-orders-institution/`, `/waiter/get-table-availability/`, `/waiter/get-table-detail/` - Retrieve open waiter orders, table availability and table details.

**Web** 
- `/web/accept-order/`, `/web/cancel-order/`, `/web/complete-order/` - Accept, cancel and complete an order. - `/web/institution-orders/canceled/`, `/web/institution-orders/completed/`, `/web/institution-orders/in-process/`, `/web/institution-orders/ready/` - Retrieve canceled, completed, in-process, and finished institutional orders. - `/web/make-order-ready/`, `/web/my-branch-id/` - Prepare an order for fulfillment and retrieve the branch ID. - `/web/takeaway-orders/canceled/`, `/web/takeaway-orders/completed/`, `/web/takeaway-orders/in-process/`, `/web/takeaway-orders/ready/` - Receive canceled, completed, in-process and ready takeaway orders.


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

If you have questions, suggestions, or would like to report a bug, feel free to contact me at my email [ulukmanmuratov@gmail.com](mailto:ulukmanmuratov@gmail.com), via Telegram [@ismailovvv001](https://t.me/ismailovvv001), or connect with me on [LinkedIn](https://www.linkedin.com/in/ismailov-uluk-92784a233/).