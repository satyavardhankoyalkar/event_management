from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),

    # Allow unauthenticated users to access registration
    path('event/<int:event_id>/register/', views.register_event, name='register_event'),
    path('event/<int:event_id>/unregister/', views.unregister_event, name='unregister_event'),

    path('event/create/', login_required(views.create_event), name='create_event'),
    path('event/<int:event_id>/edit/', login_required(views.edit_event), name='edit_event'),
    path('event/<int:event_id>/delete/', login_required(views.delete_event), name='delete_event'),
    path("my-registrations/", views.event_registrations, name="event_registrations"),

    # View registrations for an event
    path('event/<int:event_id>/registrations/', login_required(views.event_registrations), name='event_registrations'),
    
    # Filter events based on status
    path('events/filter/', views.filter_events, name='filter_events'),

    # Authentication routes
    path('login/', auth_views.LoginView.as_view(template_name='events/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path("logout/", views.user_logout, name="logout"),
    path('', views.event_list, name='event_list'),

]
