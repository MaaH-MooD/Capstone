from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from .signals import employee_created
from employee_management.models import Employee, Role, Permission, Team, Education, Address, Request, EmployeeImage



User = get_user_model()

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'description']
    
    def create(self, validated_data):
        # Ensure the name is unique (case-insensitive)
        permission_name = validated_data.get("name").strip().lower()
        if Permission.objects.filter(name__iexact=permission_name).exists():
            raise serializers.ValidationError({"name": "A permission with this name already exists."})
        
        return super().create(validated_data)
    


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description']
        
    def create(self, validated_data):
        team_name = validated_data.get("name").strip().lower()
        if Team.objects.filter(name__iexact=team_name).exists():
            raise serializers.ValidationError({"name": "A team with this name already exists."})
        
        return super().create(validated_data)
    

class RoleSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Role
        fields = ['id', 'title', 'description', 'reports_to', 'employment_type', 'permission']
        
    def create(self, validated_data):
        role_title = validated_data.get("title").strip().lower()
        if Role.objects.filter(title__iexact=role_title).exists():
            raise serializers.ValidationError({"title": "A role with this name already exists."})
        return super().create(validated_data)

class AssignRoleSerializer(serializers.Serializer):
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    employee_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all()),
        required=False  # Make it optional
    )
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=False  # Make it optional
    )


    def validate(self, data):
        if not data.get("employee_id") and not data.get("employee_ids"):
            raise serializers.ValidationError("Either 'employee_id' or 'employee_ids' must be provided.")
        if data.get("employee_id") and data.get("employee_ids"):
            raise serializers.ValidationError("Provide only 'employee_id' OR 'employee_ids', not both.")
        return data
    
class EmployeeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeImage
        fields = ["image"]
    
    def create(self, validated_data):
        # Get the currently logged-in user
        user = self.context['request'].user
        
        employee = user.employee
        
        # Check if an EmployeeImage already exists for this employee
        if hasattr(employee, 'image'):
            # If an image already exists, update it
            employee.image.image = validated_data['image']
            employee.image.save()
            return employee.image
        return EmployeeImage.objects.create(employee=employee, **validated_data)


    


    

class RequestSerializer(serializers.ModelSerializer):
    approver = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(employee__access_level__in=["Admin", "Manager"]),  # Only Admins & Managers
        required=False,
        allow_null=True,  # Explicitly allow null values
        default=None
    )
    date_requested = serializers.DateTimeField(format='%B %d, %Y', read_only=True)
    class Meta:
        model = Request
        fields = ["id", "request_type", "detail", "approver", "date_requested", "status"]
        read_only_fields = ["employee", "date_requested"]
    
    def get_fields(self):
        fields = super().get_fields()
        user = self.context['request'].user

        # If the user is not an admin or manager, hide the status field
        if not (user.is_staff or user.employee.access_level in ["Admin", "Manager"]):
            fields['status'].read_only = True  # Ensure status is read-only
            fields['status'].default = "Pending"  # Set default value to "Pending"
            fields['approver'].read_only = True

        return fields
    
    def create(self, validated_data):
        validated_data.pop('approver', None)
        # Set default status
        validated_data['status'] = 'Pending'  
        return super().create(validated_data)
        
    
    def update(self, instance, validated_data):
        """Allow only admins or managers to update status"""
        request = self.context['request']
        user = request.user

        # Prevent regular employees from updating status
        if "status" in validated_data and not (user.is_staff or user.employee.access_level in ['Admin', 'Manager']):
            validated_data.pop("status")

        return super().update(instance, validated_data)
    
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ["id", "institution", "course_of_study", "start_date", "end_date"]
        
    def create(self, validated_data):
        employee_id = self.context['employee_id']
        return Education.objects.create(employee_id=employee_id, **validated_data)


class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = ["employee_id", "country", "city"]
        
    
    def create(self, validated_data):
        employee_id = self.context['employee_id']
        return Address.objects.create(employee_id=employee_id, **validated_data)



class EmployeeSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    image = EmployeeImageSerializer(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())  # Accept role ID
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), many=True)  # Accept team IDs
    
    class Meta:
        model = Employee
        fields = ['id', 'user_id', 'phone', 'join_date', 'email', 'birth_date', 'gender', 'social_handle', 'employment_status', 'role', 'team', 'access_level', 'image', 'educations', 'address']
