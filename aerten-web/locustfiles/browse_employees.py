from locust import HttpUser, task, between

class WebSiteUser(HttpUser):
    wait_time = between(1, 5)
    token = None
    employee_ids = []  # Store valid employee IDs

    def on_start(self):
        """Authenticate and obtain JWT token before making requests"""
        response = self.client.post("/auth/jwt/create/", json={
            "username": "iviidev",  # Replace with your actual username
            "password": "iviidev"  # Replace with your actual password
        })

        if response.status_code == 200:
            self.token = response.json().get("access")
            print("Successfully authenticated")
            self.get_employee_ids()  # Fetch employee IDs after login
        else:
            print(f"Authentication failed: {response.text}")

    def get_employee_ids(self):
        """Fetch all employee IDs and store them for later use"""
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.client.get("/api/v1/employees/", headers=headers)
            
            try:
                employees = response.json()
                print(f"Employee API Parsed: {employees}")  # Debugging

                if isinstance(employees, dict) and "results" in employees:  # Handle pagination
                    employees = employees["results"]

                if not isinstance(employees, list):
                    print("Unexpected API response format:", employees)
                    return  # Exit to prevent further errors

                self.employee_ids = [emp["id"] for emp in employees if "id" in emp]
                print(f"Fetched Employee IDs: {self.employee_ids}")

            except Exception as e:
                print(f"Error parsing employee response: {e}, Response: {response.text}")


    @task(2)
    def view_employees(self):
        """Fetch employees list with authentication"""
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get("/api/v1/employees/", name='/api/v1/employees', headers=headers)
        else:
            print("No token available, skipping request")

    @task(4)
    def view_employee(self):
        """Fetch a single employee's details with authentication"""
        if self.token and self.employee_ids:
            headers = {"Authorization": f"Bearer {self.token}"}
            employee_id = self.employee_ids[0]  # Pick first valid ID
            self.client.get(f"/api/v1/employees/{employee_id}", name='/api/v1/employees/:id', headers=headers)
        else:
            print("No employee IDs available, skipping request")
