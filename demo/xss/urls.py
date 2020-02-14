from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('test', views.test, name='test'),
    path('profile', views.profile, name='profile'),
    path('admin', views.admin, name='admin'),
    path('admin_panel', views.admin_panel, name='admin_panel'),
    path('logout', views.logout_view, name='logout'),
    path('204161404348169841998158196377303846736', views.view_profiles, name='viewprofiles'),
    path('profile/update', views.update_bio, name='update_bio')
]

