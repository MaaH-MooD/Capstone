Aerten Backend

Aerten is a web application designed to manage employee roles, permissions, and team assignments within an organization. This backend is built using Django and Django REST Framework (DRF), implementing role-based access control (RBAC) to ensure secure management of employees and teams.

Features

User Authentication: Secure user registration, login, and authentication using Django's authentication system.

Role-Based Access Control (RBAC): Employees are assigned roles with specific permissions that define their access rights.

Team Management: Employees can be assigned to multiple teams.

Permission Management: Admins can create and assign permissions to roles.

Employee Management: CRUD operations for employees, including role and team assignments.

API Documentation: OpenAPI documentation using Django REST Swagger/Postman.

Technologies Used

Django - Python web framework

Django REST Framework (DRF) - API development

MYSQL - Database management

Docker - Containerization (optional)

Celery & Redis - Background task processing (optional)

JWT Authentication - Secure API authentication

Installation

1. Clone the Repository
   git clone https://github.com/your-username/aerten-backend.git
   cd aerten-backend
