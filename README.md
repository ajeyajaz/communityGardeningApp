## Community Gardening App – Backend API

This is a Django REST Framework-based backend for a community gardening platform. Users can register, create and join events, comment, and receive notifications for updates and discussions.

---

### Features

1. **User Registration & Authentication (JWT)**  
   Secure signup and login with email and password.

2. **User Profiles**  
   Users can manage personal profiles with interests and skills.

3. **Event Management**

   * Create, edit, and cancel gardening events
   * Set event capacity and track participants

4. **Event Participation**

   * Join or leave events
   * Enforce max capacity limit

5. **Commenting System**

   * Post questions/comments on event pages
   * Anyone can view the discussion

6. **Notifications API**

   * Notify users about:

     * New comments on their events
     * Event participation changes
     * Event updates

---

### ⚙️ Setup Instructions

1. **Clone the repo**

```bash
https://github.com/ajeyajaz/communityGardeningApp.git  
cd community-garden
```

2. **Create & activate virtual environment**

```bash
python -m venv venv
source venv/Scripts/activate  # or venv/bin/activate for Linux/macOS
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Apply migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser (optional)**

```bash
python manage.py createsuperuser
```

6. **Run the development server**

```bash
python manage.py runserver
```
## API Documentation

To explore and test the available API endpoints, visit the following links after running the server:

* Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
* ReDoc UI: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

These interfaces provide a complete overview of all available endpoints, request/response structures, authentication requirements, and more.


---


### API Authentication

Uses **JWT** for secure auth.

* **Register:** `POST /api/users/signup/`
* **Login:** `POST /api/users/login/`
* Include token in headers:

  ```
  Authorization: Bearer <access_token>
  ```

---

### Sample API Endpoints

#### Authentication

* `POST /api/users/signup/`
* `POST /api/users/login/`

#### 👤 Profiles

* `GET /api/users/profile/`
* `PUT /api/users/profile/update/`

#### Events

* `POST /api/events/`
* `GET /api/events/?date=2024-01-01&location=Delhi`
* `PUT /api/events/<id>/edit/`
* `POST /api/events/<id>/cancel/`

#### 🢑 Participation

* `POST /api/events/<id>/join/`
* `POST /api/events/<id>/leave/`

#### Comments

* `POST /api/comments/<event_id>/`
* `GET /api/comments/<event_id>/`

#### Notifications

* `GET /api/notifications/`

---

### Running Tests

Run all tests and save results:

```bash
python manage.py test events.tests comments.tests users.tests notifications.tests > test_results.txt
```

You’ll find test cases in:

* `events/tests/`
* `users/tests/`
* `comments/tests/`
* `notifications/tests/`

---


