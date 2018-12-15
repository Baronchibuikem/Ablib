from django.urls import path
from . import views


urlpatterns = [
    path('', views.CourseList, name='course_list'),
    path('mine/', views.ManageCourse, name='manage_course'),
    path('create/', views.CourseCreateView.as_view(), name='course_create'),
    path('<pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('<pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('<pk>/module/', views.CourseModuleUpdateView.as_view(), name='course_module_update'),
    path('module/<module_id>/content/<model_name>/create/', views.ContentCreateUpdateView.as_view(), name='module_content_create'),
    path('module/<module_id>/content/<model_name>/<id>/', views.ContentCreateUpdateView.as_view(), name='module_content_update'),
    path('content/<id>/delete/', views.ContentDeleteView.as_view(), name='module_content_delete'),
    path('module/<module_id>/', views.ModuleContentListView.as_view(), name='module_content_list'),
    path('subject/<subject>/', views.CourseList, name='course_list_subject'),
    path('<slug>/', views.CourseDetailView.as_view(), name='course_detail'),
]