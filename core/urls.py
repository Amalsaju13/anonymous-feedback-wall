from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    FeedbackGroupListCreateView,
    FeedbackGroupRetrieveUpdateDeleteView,
    FeedbackListView,
    FeedbackModerationView,
    submit_feedback
)

urlpatterns = [
    # ✅ Auth routes
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ Feedback Group
    path('groups/', FeedbackGroupListCreateView.as_view(), name='group-list-create'),
    path('groups/<int:pk>/', FeedbackGroupRetrieveUpdateDeleteView.as_view(), name='group-detail'),

    # ✅ Feedback operations
    path('groups/<int:group_id>/feedbacks/', FeedbackListView.as_view(), name='feedback-list'),
    path('feedback/<int:pk>/', FeedbackModerationView.as_view(), name='moderate-feedback'),
    path('feedback/submit/', submit_feedback, name='submit-feedback'),
]
