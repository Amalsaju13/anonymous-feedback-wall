#  Anonymous Feedback Wall – Django Backend

A robust backend system built with Django and Django REST Framework that allows administrators to create groups and receive anonymous feedback from users.

##  Objective

- Secure registration & JWT-based login for **group admins only**
- Anonymous feedback submission by anyone (no login)
- Admin-only feedback moderation & listing
- Rate limiting for spam control
- Auto-generated API documentation with Swagger & Redoc

---

##  Features

-  Admin Registration & JWT Login
-  Group CRUD APIs (admin only)
-  Anonymous Feedback Submission (open to public)
-  Feedback Listing per group (with pagination)
-  Moderation (hide/delete) for inappropriate feedback
-  IP-based Rate Limiting
-  Swagger & Redoc API Docs
-  SQLite by default (PostgreSQL compatible)
-  Bonus: `.env` support for secrets

---

##  Tech Stack

- Python 3.10+
- Django 5.x
- Django REST Framework
- Simple JWT Auth
- drf-yasg for Swagger Docs
- SQLite (PostgreSQL ready)

---

##  Project Structure

feedbackwall/
├── core/
│ ├── models.py # AdminUser, FeedbackGroup, Feedback
│ ├── serializers.py # Register, Group, Feedback serializers
│ ├── views.py # All API Views
│ ├── urls.py # Core API routes
│ ├── permissions.py # IsAdminUser custom permission
│ ├── tests.py # (Optional) Tests
├── feedbackwall/
│ ├── settings.py # Django settings
│ ├── urls.py # Includes Swagger/Redoc routes
├── db.sqlite3
├── .env.example # Sample env vars
├── requirements.txt

---

##  Installation & Setup

```bash
# Clone the repo
git clone https://github.com/your-username/anonymous-feedback-wall.git
cd anonymous-feedback-wall

# Create a virtual environment
python -m venv env
source env/bin/activate    # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
________________________________________
Environment Variables
Create a .env file or use .env.example:
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
________________________________________
 Authentication
All admin APIs require JWT Authentication.
Obtain Token
POST /api/login/
{
  "username": "admin",
  "password": "yourpassword"
}
Auth Headers
Add to request:
Authorization: Bearer <access_token>
________________________________________
 API Endpoints
Endpoint	Method	Auth	Description
/api/register/	POST	❌	Register new admin
/api/login/	POST	❌	JWT login
/api/token/refresh/	POST	❌	Refresh JWT token
/api/groups/	GET/POST	✅ Admin	List/Create groups
/api/groups/<id>/	GET/PUT/DELETE	✅ Admin	Retrieve/Update/Delete group
/api/groups/<id>/feedbacks/	GET	✅/❌	List feedback (admin sees all)
/api/feedback/submit/	POST	❌	Submit anonymous feedback
/api/feedback/<id>/	PATCH/DELETE	✅ Admin	Hide or delete a feedback
/swagger/	GET	❌	Swagger API docs
/redoc/	GET	❌	ReDoc API docs
________________________________________
Rate Limiting
To prevent spam:
•	Unauthenticated users: 5/minute
•	Authenticated users: 10/minute
•	Feedback submission endpoint: 2/minute
________________________________________
 Bonus Features
•	 Swagger & Redoc UI
•	 Modular codebase with permissions & serializers
________________________________________
 Running Tests
python manage.py test
(Write tests inside core/tests.py.)
