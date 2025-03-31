import uuid
from django.db import models
from django.contrib import admin
from django.conf import settings
from django.utils import timezone
from employee_management.validators import validate_file_size


# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    
    # Change the string representation
    def __str__(self) -> str:
        return self.name
    
    # Sort the Team object
    class Meta:
        ordering = ['name']
    
    
class Permission(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    
    # Change the string representation
    def __str__(self) -> str:
        return self.name
    
    # Sort the Permission object
    class Meta:
        ordering = ['name']

class Role(models.Model):
    
    EMPLOYEMENT_TYPE = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Associate', 'Associate'),
    ]
        
     
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    reports_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='surbodinates')
    employment_type = models.CharField(max_length=20, choices=EMPLOYEMENT_TYPE, default="Full-time")
    team = models.ManyToManyField(Team, blank=True)
    permission = models.ManyToManyField(Permission, blank=True)
    
    # Change the string representation
    def __str__(self) -> str:
        return f"{self.title} ({self.employment_type})"
    
    # Sort the Role object
    class Meta:
        ordering = ['title']
    

class Employee(models.Model):
    EMPLOYMENT_STATUS_ACTIVE = "Active"
    EMPLOYMENT_STATUS_INACTIVE = "Inactive"
    
    EMPLOYMENT_STATUS_CHOICES = [
        (EMPLOYMENT_STATUS_ACTIVE, 'Active'),
        (EMPLOYMENT_STATUS_INACTIVE, 'Inactive')
    ]
    
    GENDER_STATUS_CHOICES = [
        ("M", "Male"),
        ("F", "Female")
    ]
    
    
    ACCESS_LEVEL_CHOICES = [
        ("Admin", "Admin"),
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
        ('Guest', 'Guest')   
    ]
    
    id = models.CharField(
        primary_key=True,  # Make it the primary key
        max_length=13, 
        unique=True, 
        editable=False
    )
    phone = models.CharField(max_length=12, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    join_date = models.DateField(default=timezone.now)
    gender = models.CharField(max_length=1, choices=GENDER_STATUS_CHOICES)
    social_handle = models.CharField(max_length=255, null=True, blank=True)
    employment_status = models.CharField(max_length=50, choices=EMPLOYMENT_STATUS_CHOICES, default=EMPLOYMENT_STATUS_ACTIVE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ManyToManyField(Team, blank=True)
    access_level = models.CharField(max_length=100, choices=ACCESS_LEVEL_CHOICES, default="Employee")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    
    def __str__(self) -> str:
        full_name = f"{self.user.first_name} {self.user.last_name}"
        return full_name
    
    def __str__(self):
        return f"{self.user.username} - {self.role.title if self.role else 'No Role'} ({self.access_level})"
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    def email(self):
        return self.user.email
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    
    def save(self, *args, **kwargs):
        if not self.id:  # Generate ID only if it doesn't exist
            self.id = uuid.uuid4().hex[:12].upper()  # 13 random chars after #
        super().save(*args, **kwargs)
        

class EmployeeImage(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True, related_name="image")
    image = models.ImageField(upload_to='employee_management/images', validators=[validate_file_size])
    
    def __str__(self):
        return f"Image for {self.employee.user.username}"

class Request(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    TYPE_CHOICES = [
        ('Leave', 'Leave'),
        ('Expense', 'Expense'),
        ('Remote Work', 'Remote Work'),
        ('Other', 'Other'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='requests')
    request_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    detail =  models.TextField()
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approvals')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    date_requested = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.request_type} request by {self.employee.user.username}"

class Education(models.Model):
    institution = models.CharField(max_length=255)
    course_of_study = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="educations")

class Address(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True, related_name="address")
    
    def __str__(self):
        return f"{self.employee}'s address"