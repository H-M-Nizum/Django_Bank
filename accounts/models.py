from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# choices ar data list ar modde list akare othoba tuppal ar modde tuppol akare rakha jay.
ACCOUNT_TYPE = (
    # ('frontend', 'backend'),
    ('Savings', 'Savings'),
    ('Current', 'Current'),
)
GENDER_TYPE = (
    ('Male', 'Male'),
    ('Female', 'Female')
)


class UserBankAccountModel(models.Model):
    # user built in model, user ar modde ache username, firstname, lastname, email, password etc.
    #  user ar sathe amader moel ar onetoone relation built korchi . 
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE)
    
    # Every user have a unique account number.
    account_no = models.IntegerField(unique=True)
    
    birth_day  = models.DateField(null=True, blank = True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    
    initial_deposite_date = models.DateField(auto_now_add=True)
    
    # akjon user 12 digit porjonto and dosomik ar por 2 gor nite parbe.
    balance = models.DecimalField(default=0, max_length=12, max_digits=1000000000000, decimal_places=2)
    is_bankrupt = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.account_no)
    
    
class UserAddressModel(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    
    street_address = models.CharField(max_length = 100)
    city = models.CharField(max_length = 100)
    postal_code = models.IntegerField()
    country = models.CharField(max_length = 100)
    
    def __str__(self):
        return str(self.user.username)
    
    


