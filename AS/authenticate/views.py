# auth/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer

# Регистрация пользователя
def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationSerializer(data=request.POST)
        if form.is_valid():
            user = form.save()

            # Логиним пользователя после успешной регистрации
            login(request, user)

            # Генерация JWT токена
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Сохраняем токен в куки
            response = redirect('home')  # Перенаправляем на главную страницу
            response.set_cookie('jwt', access_token)
            return response
    else:
        form = UserRegistrationSerializer()

    return render(request, 'authenticate/signup.html', {'form': form})

# Вход пользователя
def signin_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Генерация JWT токена
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Сохраняем токен в куки
            response = redirect('home')
            response.set_cookie('jwt', access_token)
            return response
        else:
            return render(request, 'authenticate/signin.html', {'error': 'Неверные учетные данные'})
    return render(request, 'authenticate/signin.html')

# Выход пользователя
def signout_view(request):
    logout(request)
    response = redirect('signin')
    response.delete_cookie('jwt')  # Удаляем JWT токен
    return response
