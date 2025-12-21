# 🗂️ Task Management System — MVP

A **monolithic backend-first Task Management System** built with Django.  
This project is designed as a **learning-focused, production-style MVP**, emphasizing clean architecture, RESTful APIs, and core backend engineering principles.

---

## 🚀 Project Goals

- Practice **real-world backend architecture**
- Build a **modular monolith** using Django
- Implement **RESTful APIs**
- Apply **authentication & authorization**
- Prepare a strong **portfolio project** for backend roles

---

## 🧰 Tech Stack

| Layer | Technology |
|------|-----------|
| Backend | Python (Django) |
| Database | Django ORM (SQLite) |
| Frontend | HTML, Bootstrap |
| API Design | REST |
| Auth | Django Default Authentication & Authorization 

---

## ✨ Features (MVP Scope)

- ✅ User authentication (login, logout, permissions)
- ✅ Project management
- ✅ Task management (CRUD)
- ✅ User–Project relationships
- ✅ RESTful API design
- ✅ Modular app structure
- ⏳ Future-ready architecture (easy to extend)

---

## 🏗️ Project Architecture
```text
.task_manager/
├── apps/
│   ├── users/
│   ├── tasks/
│   ├── projects/
│
├── core/
│   ├── permissions.py
│   ├── mixins.py
│   ├── utils.py
│
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   ├── prod.py
```

---

## 🔐 Authentication & Authorization

- Uses **Django’s built-in authentication system**
- Session-based authentication
- Permission checks via:
  - Django permissions

---

## 🔌 API Endpoints

### 🔑 Authentication

| Method | Endpoint | Description |
|------|---------|------------|
| POST | `/api/v1/auth/login/` | User login |
| POST | `/api/v1/auth/logout/` | User logout |

---

### 👤 Users

| Method | Endpoint | Description |
|------|---------|------------|
| GET | `/api/v1/users/` | List users |
| GET | `/api/v1/users/{id}/` | Retrieve user |

---

### 📁 Projects

| Method | Endpoint | Description |
|------|---------|------------|
| GET | `/api/v1/projects/` | List projects |
| POST | `/api/v1/projects/` | Create project |
| GET | `/api/v1/projects/{id}/` | Retrieve project |
| PUT | `/api/v1/projects/{id}/` | Update project |
| DELETE | `/api/v1/projects/{id}/` | Delete project |

---

### ✅ Tasks

| Method | Endpoint | Description |
|------|---------|------------|
| GET | `/api/v1/tasks/` | List tasks |
| POST | `/api/v1/tasks/` | Create task |
| GET | `/api/v1/tasks/{id}/` | Retrieve task |
| PUT | `/api/v1/tasks/{id}/` | Update task |
| DELETE | `/api/v1/tasks/{id}/` | Delete task |

---

## 🗃️ Database Design

- SQLite (development-friendly)
- ORM-driven models
- Relationships:
  - User ↔ Projects (Many-to-Many)
  - Project ↔ Tasks (One-to-Many)
  - User ↔ Tasks (Ownership / Assignment)
