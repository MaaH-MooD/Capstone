from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description"]
    list_editable = ["name", "description"]
    list_per_page = 10
    
    
    
@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "employment_type", "get_permission"]
    list_editable = ["title", "description", "employment_type"]
    
        # Many to Many relationship
    def get_permission(self, role):
        return ", ".join([permission.name for permission in role.permission.all()])
    get_permission.short_description = 'Permission'
    
@admin.register(models.Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description"]
    list_editable = ["name", "description"]
    

@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email", "phone", "birth_date", "join_date", "gender", "social_handle", "employment_status", "get_role", "get_team", "access_level"]
    list_editable = ["phone", "birth_date", "join_date", "gender", "social_handle", "employment_status", "access_level"]
    list_per_page = 10
    list_select_related = ["role", "user"]
    search_fields = ["first_name__istartswith", "last_name__istartswith"]
    
    
    def get_role(self, employee):
        return employee.role.title
    
    
    # Many to Many relationship
    def get_team(self, employee):
        return ", ".join([team.name for team in employee.team.all()])
    get_team.short_description = 'Team'
    

@admin.register(models.Request)    
class RequestAdmin(admin.ModelAdmin):
    list_display = ["id", "request_type", "detail", "approver", "status", "date_requested"]
    
    
@admin.register(models.Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["id", "institution", "course_of_study", "start_date", "end_date", "employee"]
    list_editable = ["institution", "course_of_study"]
    list_select_related = ["employee"]
    
@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["employee_id", "country", "city", "employee"]
    list_select_related = ["employee"]