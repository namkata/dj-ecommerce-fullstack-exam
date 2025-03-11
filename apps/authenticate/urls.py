from django.urls import path
from apps.authenticate import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # # Password reset URLs
    # path("password-reset/", views.password_reset_view, name="password_reset"),
    # path("password-reset/done/", views.password_reset_done_view, name="password_reset_done"),
    # path("password-reset/<uidb64>/<token>/", views.password_reset_confirm_view, name="password_reset_confirm"),
    # path("password-reset/complete/", views.password_reset_complete_view, name="password_reset_complete"),
    # # Password change URLs
    # path("password-change/", views.password_change_view, name="password_change"),
    # path("password-change/done/", views.password_change_done_view, name="password_change_done"),
    # Profile management
    path("profile/", views.profile_view, name="profile"),
    # path("profile/edit/", views.profile_edit_view, name="profile_edit"),
]
