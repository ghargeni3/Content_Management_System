from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    AuthUserRegistrationView,
    AuthUserLoginView,
    UserListView,
    ContentRegistrationView,
    ContentListView,
    ContentSearchView
)

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register', AuthUserRegistrationView.as_view(), name='register'),
    path('login', AuthUserLoginView.as_view(), name='login'),
    path('users', UserListView.as_view(), name='users'),
    path('content/create',ContentRegistrationView.as_view(), name='create_content'),
    path('contents',ContentListView.as_view(), name='contents'),
    path('contents/<str:uid>',ContentListView.as_view(), name='contents_uid'),
    path("search/<str:key>", ContentSearchView.as_view(), name="search_results"),
]
