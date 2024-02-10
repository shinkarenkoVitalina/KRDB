"""
URL configuration for Done project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index),
    path('rp_space', views.index, name = "rp_space"),
    path('desk/<int:id_rp>/', views.desk, name = 'desk'),
    path('create_workspace/', views.create_workspace, name='create_workspace'),
    path('create_desk/<int:id_ws>/', views.create_desk, name='create_desk'),
    path('logout_user/', views.LogoutUser, name='logout_user'),
    path('desk_space/<int:id_ws>/<int:desk_id>/', views.user_desk, name='desk_space'),
    path('createlist/<int:id_ws>/<int:desk_id>/', views.create_list, name='createlist'),
    path('deletews/<int:id_ws>/', views.DeleteSpace, name='deletews'),
    path('deletedesk/<int:id_ws>/<int:id_desk>/', views.DeleteDesk, name = 'deletedesk'),
    path('createcard/<int:id_ws>/<int:desk_id>/<int:list_id>/', views.create_card, name = "createcard"),
    path('updatews/<int:id_ws>', views.update_space, name = "updatews"),
    path('updatedesk/<int:id_ws>/<int:desk_id>', views.update_desk, name = "updatedesk"),
    path('updatedesk_type/<int:id_ws>/<int:desk_id>', views.update_desk_type, name = "updatedesk_type"),
    path('deletelist/<int:id_ws>/<int:desk_id>/<int:list_id>/', views.DeleteList, name = "deletelist"),
    path('deletetask/<int:id_ws>/<int:desk_id>/<int:task_id>/', views.DeleteTask, name = "deletetask"),
    path('createchecklist/<int:id_ws>/<int:desk_id>/<int:card_id>/', views.create_checklist, name = "createchecklist"),
    path('getdeadline/<int:id_ws>/<int:desk_id>/<int:task_id>/', views.GetDeadlineTask, name = "getdeadline"),
    path('createaction/<int:id_ws>/<int:desk_id>/<int:checklist_id>/', views.create_action, name = 'createaction'),
]
