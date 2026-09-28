# HireHub – Job Recruitment Platform API

HireHub is a backend API for a job recruitment platform built with **FastAPI** and **PostgreSQL**. It provides authentication, role-based access control, job management, job search, and application management features for candidates, recruiters, and administrators.

## 🚀 Features

* User registration and login
* JWT-based authentication
* Password hashing with bcrypt
* Role-based access control
* Candidate and student job applications
* Recruiter job creation and management
* Job ownership protection
* Job search and filtering
* Pagination and sorting
* Application tracking
* Application status workflow
* PostgreSQL database integration
* Interactive Swagger API documentation
* Environment variable configuration using `.env`

## 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy**
* **Pydantic**
* **JWT**
* **bcrypt**
* **OAuth2**
* **Uvicorn**
* **Git & GitHub**

## 📁 Project Structure

```text
HireHub/
│
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── security.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── models/
│   │   └── models.py
│   │
│   ├── routers/
│   │   ├── applications.py
│   │   ├── job.py
│   │   └── user.py
│   │
│   └── schemas/
│       ├── application.py
│       ├── jobs.py
│       └── user.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔐 User Roles

### Candidate / Student

Candidates can:

* Register and log in
* View available jobs
* Search and filter jobs
* Apply for jobs
* View their own applications
* Track application status

### Recruiter

Recruiters can:

* Log in
* Create jobs
* Update their own jobs
* Delete their own jobs
* View applications for their jobs
* Update candidate application status

### Admin

Administrators have elevated permissions for managing the platform and can perform administrative job-management operations.

## 📊 Application Workflow

Applications follow a controlled status workflow:

```text
Applied
   ↓
Shortlisted
   ↓
Interview
   ↓
Selected
```

An application can also be rejected during the recruitment process:

```text
Applied → Rejected
Shortlisted → Rejected
Interview → Rejected
```

Invalid status transitions are rejected by the API.

## 🔎 Job Search

The API supports searching and filtering jobs using:

* Keyword
* Location
* Job type
* Skills

Pagination and sorting are also supported.

Example:

```text
/jobs/search/?keyword=python&page=1&limit=10&sort=latest
```

## 🔑 Authentication

HireHub uses **JWT Bearer Authentication**.

After logging in, the generated access token can be used to access protected endpoints.

In Swagger:

1. Open `/docs`
2. Click **Authorize**
3. Enter the authentication credentials/token
4. Access protected endpoints

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/prachibhoyar982/Hirehub.git
cd HireHub
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/Hirehub
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do not commit the `.env` file to GitHub.

### 6. Start the server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## 📚 API Documentation

Once the server is running, interactive Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Alternative documentation:

```text
http://127.0.0.1:8000/redoc
```

## 🧪 API Testing

The API has been tested using Swagger UI, including:

* Authentication
* Role-based authorization
* Job CRUD operations
* Job search and filtering
* Pagination
* Sorting
* Job ownership
* Job applications
* Duplicate application prevention
* Application status updates
* Invalid status transitions
* Unauthorized access scenarios
* Missing resource errors

## 🔒 Security

Sensitive configuration is stored using environment variables.

The repository excludes:

```text
.env
venv/
__pycache__/
*.pyc
```

Passwords are hashed before being stored, and protected endpoints require JWT authentication.

## 🎯 Future Improvements

Possible future additions include:

* Frontend application
* Resume upload
* Candidate profiles
* Recruiter dashboard
* Email notifications
* Advanced job recommendations
* Application analytics
* Production deployment
* Automated tests with Pytest

## 👩‍💻 Author

**Prachi Bhoyar**

BTech Computer Science & Engineering

GitHub: `prachibhoyar982`

---

⭐ If you find this project useful, feel free to explore the repository.
