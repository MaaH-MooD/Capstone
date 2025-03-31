from locust import HttpUser, task, between
from random import randint

class WebSiteUser(HttpUser):
    wait_time = between(1, 5)
    token = None  # Stores the JWT token

    def on_start(self):
        """Authenticate and obtain JWT token before making requests"""
        response = self.client.post("/auth/jwt/create/", json={
            "username": "iviidev",  # Replace with your actual username
            "password": "iviidev"  # Replace with your actual password
        })
        
        if response.status_code == 200:
            self.token = response.json().get("access")
            print("Successfully authenticated")
        else:
            print(f"Authentication failed: {response.text}")

    @task(2)
    def view_teams(self):
        """Fetch employees list with authentication"""
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get("/api/v1/permissions/", name='/api/v1/permissions', headers=headers)
        else:
            print("No token available, skipping request")

    @task(4)
    def view_team(self):
        """Fetch a single employee's details with authentication"""
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            permission_id = randint(1, 8)
            self.client.get(f"/api/v1/permissions/{permission_id}/", name='/api/v1/permissions/:id', headers=headers)
        else:
            print("No token available, skipping request")