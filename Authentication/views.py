from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def SignUp(request):
     if request.user.is_authenticated:
          return redirect("index")
     else:
          form = UserForm()
          if request.method == "POST":
               form = UserForm(request.POST)
               if form.is_valid():
                    form.save()
                    return render(request, "index.html")

          context = {'form':form}
          return render(request, 'signup.html', context)

def SignIn(request):
     if request.user.is_authenticated:
          return redirect("index")
     else:
          if request.method == "POST":
               username = request.POST.get('username')
               password = request.POST.get('password1')

               user = authenticate(request, username=username, password=password)
               if user is not None:
                    login(request, user)
                    return redirect("index")
               else:
                    messages.info(request, "Enter Correct Information")

          return render(request, 'signin.html')

def signout(request):
     logout(request)
     return redirect('signin')