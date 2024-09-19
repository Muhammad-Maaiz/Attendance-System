from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

def loginpage(request):
    error = ""
    if request.method == "POST":
        # Get username and password from login form
        username = request.POST.get('username')
        password = request.POST.get('password')
        # check user is authenticate
        user=authenticate(request,username=username,password=password)
        # if authenticate then login and else show error
        if user is not None:
            login(request,user)
            return redirect('markattandence')   # After login redirect to home page
        else:
            error = "Username or Password is Invalid"

    return render(request, 'login.html', {'error':error})

def signuppage(request):
    error = ""
    if request.method == "POST":
        # Get username, email, and password from signup form
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            error = "Username is already taken. Please choose a different username."
        
        # Check if email already exists
        elif User.objects.filter(email=email).exists():
            error = "Email is already in use. Please choose a different email."
        
        else:
            # Add User data to User Model
            user_data = User.objects.create_user(username=username, email=email, password=password)
            user_data.save()
            return redirect("login")  # Redirect to login page

    return render(request, "signup.html", {'error': error})
