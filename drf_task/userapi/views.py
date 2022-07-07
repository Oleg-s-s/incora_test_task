from django.contrib.auth import authenticate, login, logout
from rest_framework import status, generics
from rest_framework.response import  Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .utils import get_tokens_for_user
from .serializers import RegistrationSerializer, UserGetSerializer, UserUpdateSerializer
from .models import MyUser



class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)

class UserInfoView(generics.RetrieveAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserGetSerializer
    permission_classes = (IsAuthenticated,)

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated,)