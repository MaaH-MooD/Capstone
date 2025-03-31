# from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import get_user_model
from model_bakery import baker
from employee_management.models import Employee, Role, Team
import pytest
import logging


# Fixtures for EmployeeViewSet
@pytest.fixture
def create_employee(api_client):
    def do_create_employee(employee):
        return api_client.post("/api/v1/employees/", employee)
    return do_create_employee

@pytest.fixture
def update_employee(api_client):
    def do_update_employee(id, employee):
        return api_client.patch(f'/api/v1/employees/{id}/', employee)
    return do_update_employee

@pytest.fixture
def delete_employee(api_client):
    def do_delete_employee(id):
        return api_client.delete(f'/api/v1/employees/{id}/')
    return do_delete_employee

@pytest.fixture
def retrieve_employee(api_client):
    def do_retrieve_employee(id):
        return api_client.get(f'/api/v1/employees/{id}/')
    return do_retrieve_employee


# @pytest.fixture
# def get_me(api_client):
#     def do_get_me():
#         return api_client.get('/api/v1/employees/me/')
#     return do_get_me

# @pytest.fixture
# def update_me(api_client):
#     def do_update_me(data):
#         return api_client.put('/api/v1/employees/me/', data)
#     return do_update_me

@pytest.fixture
def me_employee(api_client):
    def do_me_employee(method="GET", data=None):
        if method == "GET":
            return api_client.get("/api/v1/employees/me/")
        return api_client.put("/api/v1/employees/me/", data)
    return do_me_employee

@pytest.fixture
def assign_role(api_client):
    def do_assign_role(data):
        return api_client.post('/api/v1/employees/assign_role/', data)
    return do_assign_role



@pytest.mark.django_db
class TestRetrieveEmployee:
    def test_if_employee_exists_returns_200(self, retrieve_employee, authenticate):
        
        user = authenticate(is_staff=False)
        # employee = baker.make(Employee, user=user)
        employee, _ = Employee.objects.get_or_create(user=user)
        
        
        response = retrieve_employee(employee.id)
        
        assert response.status_code == status.HTTP_200_OK
        
        assert response.data["id"] == employee.id
        assert response.data["user_id"] == employee.user.id
    
    def test_if_employee_does_not_exists_return_404(self, retrieve_employee, authenticate):
        
        user = authenticate(is_staff=False)
        respose = retrieve_employee(99999)
        
        assert respose.status_code == status.HTTP_404_NOT_FOUND



@pytest.mark.django_db
class TestUpdateEmployee:
    def test_if_user_is_anonymous_returns_401(self, update_employee, authenticate):
        
        User = get_user_model()
        user = baker.make(User)
        
        employee, _ = Employee.objects.get_or_create(user=user)
        team = baker.make(Team)
        data = {"gender": "F", "team": [team.id]}
        
        
        response = update_employee(employee.id, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_not_admin_returns_403(self, authenticate,update_employee):
        user = authenticate(is_staff=False)
        employee, _ = Employee.objects.get_or_create(user=user)
        team = baker.make(Team)
        data = {"gender": "F", "team": [team.id]}
        
        
        response = update_employee(employee.id, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_if_user_provides_invalid_data_returns_400(self, authenticate, update_employee):
        user = authenticate(is_staff=True)
        employee, _ = Employee.objects.get_or_create(user=user)
        data =  {"gender": "F", "team": 123}
        
        response = update_employee(employee.id, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        
    def test_if_user_provides_valid_data_returns_200(self, authenticate, update_employee):
        user = authenticate(is_staff=True)
        team = baker.make(Team)
        employee, _ = Employee.objects.get_or_create(user=user)
        data = {"gender": "F", "team": [team.id]}
        response = update_employee(employee.id, data)
        print(response.data)
        
        assert response.status_code == status.HTTP_200_OK
        employee.refresh_from_db()
        assert team in employee.team.all()
    
    def test_if_employee_does_not_exist_returns_404(self, authenticate, update_employee):
        
        authenticate(is_staff=True)
        team = baker.make(Team)
        data = {"gender": "F", "team": [team.id]}
        
        response = update_employee(9999999, data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        

@pytest.mark.django_db
class TestDeletePermission:
    def test_if_user_is_anonymous_returns_401(self, delete_employee):
        
        # Create an employee without authenticating a user
        User = get_user_model()
        user = baker.make(User) 
        (employee, _) = Employee.objects.get_or_create(user=user)
        response = delete_employee(employee.id)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    
    def test_if_user_is_not_admin_returns_403(self, authenticate, delete_employee,):
        user = authenticate(is_staff=False)
        (employee, _) =  Employee.objects.get_or_create(user=user)
        
        response = delete_employee(employee.id)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        
    def test_if_employee_exists_return_204(self, authenticate, delete_employee):
        user = authenticate(is_staff=True)
        (employee, _) =  Employee.objects.get_or_create(user=user)

        response = delete_employee(employee.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        
    def test_if_invalid_id_returns_404(self, authenticate, delete_employee):
        authenticate(is_staff=True)        
        response = delete_employee(9999999)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND