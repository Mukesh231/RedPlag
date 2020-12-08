from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .models import Organisation, CustomUser, CustomUserManager
from .forms import CustomUserCreationForm, CustomUserChangeForm


def start (request):
    """!
    Redirects to home page

    @param request HTTP request
    @return render() function which creates the HttpResponse that is sent back to the browser

    """
    return render(request, 'start.html')


@login_required
def home(request):

    """!
    Redirects to home page

    @param request HTTP request
    @return render() function which creates the HttpResponse that is sent back to the browser

    
    
    """
    return render(request, 'home.html')

def signup(request):
    """!
    Redirects to signup page.

    Adds a User account to the database if registration is succesful, else provides the user with an empty sign up form

    @param request HTTP request
    @return render() function which creates the HttpResponse that is sent back to the browser

    
    
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('org_name')
            code = form.cleaned_data.get('org_code')
            try:
                validator = Organisation.objects.get(organame=name)    
                try:
                    validator2 = Organisation.objects.get(orgacode=code)
                    form.save()
                    username = form.cleaned_data.get('username')
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(username=username, password=raw_password)
                    login(request, user)
                    messages.success(request, f'Account created for {username}!')
                    return redirect('home')
                except:
                    messages.error(request, f'Organisation passcode does not match :(')
                    form = CustomUserCreationForm()
                    return render(request, 'signup.html', {'form': form})
            except:
                messages.error(request, f'Looks like your organisation has not registered with us :(')
                form = CustomUserCreationForm()
                return render(request, 'signup.html', {'form': form})

    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def profile(request):
    """!
    Redirects to the user profile page.

    This function requires the user to be logged in to the system, to be avaliable for access.

    @param request HTTP request
    @return render() function which creates the HttpResponse that is sent back to the browser    
    """
    return render(request, 'profile.html')




def login_view(request):
    """!
    Redirects to login page.

    Redirects the user to the home page only upon succesful login, else redirects to login page again.

    @param request HTTP request
    @return render() function which creates the HttpResponse that is sent back to the browser
   
    """
    if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(username=username, password=password)
          if user is not None:
              if user.is_active:
                  login(request, user)
                  # Redirect to index page.
                  return redirect('home')
              else:
                  # Return a 'disabled account' error message
                  return HttpResponse("You're account is disabled.")
          else:
              # Return an 'invalid login' error message.
              messages.error(request, f'Invalid Username or Password, Try again!!')
              return render(request,'login.html', {})
    else:
        # the login is a  GET request, so just show the user the login form.
        return render(request,'login.html', {})



@login_required
def logout_view(request):
    """!
    Logs the user out of the system and redirects to login page.

    This function requires the user to be logged in to the system, to be avaliable for access.

    @param request HTTP request
    @return render() function which creates the HttpResponse that is sent back to the browser

    
    """
    logout(request)
        # Redirect back to index page.
    return render(request, 'login.html', {})