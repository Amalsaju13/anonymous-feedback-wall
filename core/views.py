from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions, mixins, filters
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle

from .models import AdminUser, FeedbackGroup, Feedback
from .serializers import RegisterSerializer, FeedbackGroupSerializer, FeedbackSerializer
from .permissions import IsAdminUser


# ✅ Custom throttle class
class CustomThrottle(UserRateThrottle):
    rate = '2/min'  # Limit to 2 feedback submissions per minute


# ✅ Utility to get IP address
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


# ✅ Admin registration
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Admin registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Create/List feedback groups
class FeedbackGroupListCreateView(generics.ListCreateAPIView):
    queryset = FeedbackGroup.objects.all()
    serializer_class = FeedbackGroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# ✅ Get/Update/Delete a group
class FeedbackGroupRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeedbackGroup.objects.all()
    serializer_class = FeedbackGroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


# ✅ Submit anonymous feedback (public)
@api_view(['POST'])
@throttle_classes([CustomThrottle])
def submit_feedback(request):
    data = request.data.copy()
    data['ip_address'] = get_client_ip(request)

    serializer = FeedbackSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ List feedbacks for a group
class FeedbackListView(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['-submitted_at']

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        group = get_object_or_404(FeedbackGroup, id=group_id)

        if self.request.user.is_authenticated and getattr(self.request.user, 'is_admin', False):
            return Feedback.objects.filter(group=group)
        else:
            return Feedback.objects.filter(group=group, is_hidden=False)


# ✅ Hide/Delete feedback (admin only)
class FeedbackModerationView(mixins.DestroyModelMixin,
                             mixins.UpdateModelMixin,
                             GenericAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
