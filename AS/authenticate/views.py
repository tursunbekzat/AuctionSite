from django.contrib.auth.forms import UserCreationForm
from rest_framework import generics, permissions, response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer, UserSerializer, TokenSerializer
from .models import User
from django.contrib.auth import login, authenticate, authenticate
from django.shortcuts import render, redirect
from django.http import JsonResponse


# class RegistrationView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegistrationSerializer

# class LoginView(generics.GenericAPIView):
#     serializer_class = UserSerializer

#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         user = authenticate(username=username, password=password)

#         if user:
#             refresh = RefreshToken.for_user(user)
#             return response.Response({"refresh": str(refresh), "access": str(refresh.access_token)})

#         return response.Response({"detail": "Invalid credentials"}, status=401)

# class UserView(generics.RetrieveAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserSerializer

#     def get_object(self):
#         return self.request.user

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Или другая страница после успешной регистрации
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Или другая страница после успешного входа
        else:
            return JsonResponse({'error': 'Неверные учетные данные'}, status=400)
    return render(request, 'auth/signin.html')