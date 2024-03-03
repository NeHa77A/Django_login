from django.contrib.auth import authenticate,login, logout
from django.shortcuts import redirect, render
from django.http import HttpResponse
# django inbuild function to use database
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username):
            messages.error(request, "Username Already Exist!")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request,"Email Already Registered!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "UserName Must be under 20 characters")

        if password1 != password2:
            messages.error(request,"Password Did not match")

        if not username.isalnum():
            messages.error(request,"Username Must be contain Number with Alphabet")
            return redirect('home')


        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = first_name
        myuser.last_name = last_name

        myuser.save()
        messages.success(request,"Your Account has been successfully Created ")
        return redirect('signin')


    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']

        # Check authenticated or not my django
        user = authenticate(username=username, password =password1)

        # if the credintial are correct
        if user is not None:
            login(request, user)
            first_name = user.first_name
            return render(request, "authentication/index.html", {'first_name': first_name})
        else:
            messages.error(request, "Credential are not correct")
            return redirect('home')
    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully! ")
    return redirect('home')