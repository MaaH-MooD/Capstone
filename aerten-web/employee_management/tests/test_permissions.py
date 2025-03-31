from django.contrib.auth.models import User
from rest_framework import status
from model_bakery import baker
from employee_management.models import Permission
import pytest

@pytest.fixture
def create_permission(api_client):
    def do_create_permission(permission):
        return api_client.post("/api/v1/permissions/", permission)
    return do_create_permission


@pytest.fixture
def update_permission(api_client):
    def do_update_permission(id, permission):
        return api_client.patch(f'/api/v1/permissions/{id}/', permission)
    return do_update_permission

@pytest.fixture
def delete_permission(api_client):
    def do_delete_permission(id):
        return api_client.delete(f'/api/v1/permissions/{id}/')
    return do_delete_permission

@pytest.fixture
def retrieve_permission(api_client):
    def do_retrieve_permission(id):
        return api_client.get(f'/api/v1/permissions/{id}/')
    return do_retrieve_permission
    

@pytest.mark.django_db
class TestCreatePermission:
    # @pytest.mark.skip
    def test_if_user_is_anonymous_returns_401(self, create_permission):
        response = create_permission({"name": "a", "description": "aaaaaaa"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    
    def test_if_user_is_not_admin_returns_403(self, authenticate, create_permission):
        # Act
        authenticate(is_staff=False)
        response = create_permission({"name": "a", "description": "aaaaaaa"})
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    # User is authenticated and is admin but data is invalid
    def test_if_data_is_invalid_returns_400(self, authenticate, create_permission):
        # Act
        authenticate(is_staff=True)
        response = create_permission({"name": "", "description": "aaaaaaa"})
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["name"] is not None
        
    def test_if_data_is_valid_returns_201(self, authenticate, create_permission):
        # Act
        authenticate(is_staff=True)
        response = create_permission( {"name": "a", "description": "aaaaaaa"})
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("id") > 0
        
        
@pytest.mark.django_db
class TestRetrievePermission:
    def test_if_permission_exists_returns_200(self, retrieve_permission):
        permission = baker.make(Permission)
        
        response = retrieve_permission(permission.id)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": permission.id,
            "name": permission.name,
            "description": permission.description
        }
    
    def test_if_permission_does_not_exists_return_404(self, retrieve_permission):
        respose = retrieve_permission(99999)
        
        assert respose.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestUpdatePermission:
    def test_if_user_is_anonymous_returns_401(self, update_permission):
        permission = baker.make(Permission)
        data =  {"name": "a", "description": "aaaaaaa"}
        
        response = update_permission(permission.id, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_if_user_is_not_admin_returns_403(self, authenticate, update_permission):
        permission = baker.make(Permission)
        data = {"name": "updated_name", "description": "updated_description"}
        authenticate(is_staff=False)
        response = update_permission(permission.id, data)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_if_user_provides_invalid_data_returns_400(self, authenticate, update_permission):
        permission = baker.make(Permission)
        data = {"name": "", "description": ""}  # Invalid input
        
        authenticate(is_staff=True)
        response = update_permission(permission.id, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_if_user_provides_valid_data_returns_200(self, authenticate, update_permission):
        permission = baker.make(Permission)
        data = {"name": "new_name", "description": "updated_description"}
        
        authenticate(is_staff=True)
        response = update_permission(permission.id, data)
        
        assert response.status_code == status.HTTP_200_OK
        permission.refresh_from_db()
        assert permission.name == "new_name"
    
    def test_if_permission_does_not_exist_returns_404(self, authenticate, update_permission):
        data = {"name": "random", "description": "random"}
        
        authenticate(is_staff=True)
        response = update_permission(9999999, data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
@pytest.mark.django_db
class TestDeletePermission:
    def test_if_user_is_anonymous_returns_401(self, delete_permission):
        permission = baker.make(Permission)
        response = delete_permission(permission.id)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    
    def test_if_user_is_not_admin_returns_403(self, authenticate, delete_permission):
        authenticate(is_staff=False)
        permission = baker.make(Permission)
        response = delete_permission(permission.id)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_if_permission_exists_return_204(self, authenticate, delete_permission):
        authenticate(is_staff=True)
        permission = baker.make(Permission)
        
        response = delete_permission(permission.id)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
    def test_if_invalid_id_returns_404(self, authenticate, delete_permission):
        authenticate(is_staff=True)        
        response = delete_permission(9999999)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND