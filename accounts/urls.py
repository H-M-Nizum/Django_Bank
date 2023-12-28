from django.urls import path
from . import views

urlpatterns = [
   path('register/',  views.UserRegistrationViews.as_view(), name='register'),
   path('login/',  views.Userloginviews.as_view(), name='login'),
   path('logout/',  views.userlogoutview.as_view(), name='logout'),
   path('profile/',  views.UserBankAccountUpdateView.as_view(), name='profile'),
   path('pass_change/', views.passward_change, name='passwordChange'),
]
