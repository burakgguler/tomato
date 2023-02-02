from django.urls import path

from account.api.views import ChangePasswordView, CreateUserView, ProfileView

app_name = 'account'
urlpatterns = [
    path('me/', ProfileView.as_view(), name='me'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('register/', CreateUserView.as_view(), name='register')
]
