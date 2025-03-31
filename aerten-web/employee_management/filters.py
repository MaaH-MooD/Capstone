import django_filters
from .models import Role, Employee, Request

class RoleFilter(django_filters.FilterSet):
    class Meta:
        model = Role
        fields = {
            "title": ["exact", "icontains"],
            "reports_to": ["exact"],
        }

class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = {
            "user__first_name": ["exact", "icontains"],
            "user__last_name": ["exact", "icontains"],
            "role": ["exact"],
            "gender": ["exact"],
            "employment_status": ["exact"],
            "team": ["exact"]
        }

class RequestFilter(django_filters.FilterSet):
    class Meta:
        model = Request
        fields = {
            "status": ["exact"],
            "date_requested": ["icontains"] 
        }