from django.urls import path

from account.api.views import ProfileView, ChangePasswordView

app_name = 'account'
urlpatterns = [
    path('me/', ProfileView.as_view(), name='me'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password')
]
