from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView

# change passwword
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
# from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
# Create your views here.

# send email
from transactions.views import send_transaction_email
 

def passward_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SetPasswordForm(user = request.user, data=request.POST)
            if form.is_valid():
                form.save()
                send_transaction_email(request.user, 'pass change', "password change Message", "pass_change_email.html")
                # password update korbe
                update_session_auth_hash(request, form.user)
                return redirect('profile')
        else:
            form = SetPasswordForm(user=request.user)

        return render(request, 'passwordChange.html', {'form': form})
    else:
        return redirect('login')

class UserRegistrationViews(FormView):
    template_name = 'user_regostration.html'
    form_class = UserRegistrationForm
    success_url =reverse_lazy('register')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form) # form_valid functions call hobe jodi sob thik thake
    
    
    
class Userloginviews(LoginView):
    template_name = 'user_login.html'
    
    def get_success_url(self):
        return reverse_lazy('home')
    
# class userlogoutview(LogoutView):
#     def get_success_url(self):
#         if self.request.user.is_authenticated:
#             logout(self.request)
#         return redirect('home')

class userlogoutview(View):
    def get(self, request):
        logout(request)
        return redirect('home')

# profile view
class UserBankAccountUpdateView(View):
    template_name = 'profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})