from rest_framework import generics, mixins

from .models import User
from .serializers import UserSerializer


class UserSignupView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
