from django.contrib import admin
from django.urls import path
from students import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.student_list), 
    path('add/', views.add_student),  
    path('delete/<int:id>/', views.delete_student),
    path('edit/<int:id>/', views.edit_student),
    path('login/', views.login_user),
    path('logout/', views.logout_user),
    path('marks/<int:id>/', views.view_marks),
    path('marks/edit/<int:id>/', views.edit_marks),
    path('marks/delete/<int:id>/', views.delete_marks),
    path('dashboard/', views.dashboard),  
]