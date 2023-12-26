from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserBankAccountModel, UserAddressModel

ACCOUNT_TYPE = (
    # ('frontend', 'backend'),
    ('Savings', 'Savings'),
    ('Current', 'Current'),
)
GENDER_TYPE = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

# 3 ta model ar data ke akta form a show korar jonne usercreationform use kora hoyeche
class UserRegistrationForm(UserCreationForm):
    # UserBankAccountModel ar fields jekhan a user data dibe
    birth_day  =forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    
    # UserAddressModel ar fields jekhan a user data dibe
    street_address = forms.CharField(max_length = 100)
    city = forms.CharField(max_length = 100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length = 100)
    
    # Meta class extra characterastic add kore.
    class Meta:
        model = User
        
        # User model and UserBankAccountModel, UserAddressModel model ar fields ja form a display hobe.
        fields = ['username', 'first_name', 'last_name', 'email',  'account_type','birth_day', 'gender', 'street_address', 'city', 'postal_code', 'country']
        
        
    # jehetu ak e form the tinta model a data save hobe .. so save function ta handel korte hobbe.
    
    def save(self, commit= True):
        user =  super().save(commit=False)
        if commit == True:
            user.save() # user model a data save hobe
            
            
        
            account_type = self.cleaned_data.get('account_type')
            birth_day = self.cleaned_data.get('birth_day')
            gender = self.cleaned_data.get('gender')
            
            street_address = self.cleaned_data.get('street_address')
            city = self.cleaned_data.get('city')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')
            
            # UserAddressModel model a data save hobe
            UserAddressModel.objects.create(
                user = user,
                street_address = street_address,
                city = city,
                postal_code = postal_code,
                country = country,
            )
            
            # UserBankAccountModel model a data save hobe
            UserBankAccountModel.objects.create(
                user = user,
                account_type = account_type,
                birth_day=birth_day, 
                gender = gender, 
                account_no = 1000000 + user.id
            )
            
            
        return user
    
    
    # Backend theke inputfield a style. tailwind css ar style class .
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })



# user ar data update or edit ar jonnne createdd form 

class UserUpdateForm(forms.ModelForm):
    birth_day = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length= 100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


    #  fields a r input tag a backend theke style add.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
        # jodi user er account thake 
        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
                
            except UserBankAccountModel.DoesNotExist:
                user_account = None
                user_address = None

            if user_account:
                self.fields['account_type'].initial = user_account.account_type
                self.fields['gender'].initial = user_account.gender
                self.fields['birth_day'].initial = user_account.birth_day
                self.fields['street_address'].initial = user_address.street_address
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['country'].initial = user_address.country


    # update ar por data save korara jonnne function
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account, created = UserBankAccountModel.objects.get_or_create(user=user) # jodi account thake taile seta jabe user_account ar jodi account na thake taile create hobe ar seta created er moddhe jabe
            user_address, created = UserAddressModel.objects.get_or_create(user=user) 

            user_account.account_type = self.cleaned_data['account_type']
            user_account.gender = self.cleaned_data['gender']
            user_account.birth_day = self.cleaned_data['birth_day']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return user