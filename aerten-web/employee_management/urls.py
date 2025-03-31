from django.urls import path
# from rest_framework.routers import SimpleRouter, DefaultRou
from rest_framework_nested import routers
from . import views
from pprint import pprint


router = routers.DefaultRouter()
router.register('permissions', views.PermissionViewSet)
router.register('teams', views.TeamViewSet)
router.register('roles', views.RoleViewSet)
router.register('employees', views.EmployeeViewSet)
router.register('requests', views.RequestViewSet, basename='requests')
router.register('employee-image', views.EmployeeImageViewSet, basename='employeeimage')



employees_router = routers.NestedDefaultRouter(router, 'employees', lookup='employee')
employees_router.register('educations', views.EducationViewSet, basename='employee-educations')
employees_router.register('address', views.AddressViewSet, basename='employee-address')


urlpatterns = router.urls + employees_router.urls