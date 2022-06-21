from django.shortcuts import render
from accounts.forms import RegistrationForms
from accounts.models import Account

def login(request):
    return render(request, 'accounts/login.html')

def logout(request):
    return render(request, 'accounts/logout.html')

def register(request):

    if request.method == 'POST':
        form = RegistrationForms(request.POST)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['first_name']
            email = form.cleaned_data['first_name']
            phone_number = form.cleaned_data['first_name']
            password = form.cleaned_data['password']
            # confirm_password = form.cleaned_data['confirm_password']
            username = email.split('@')[0]

            user = Account.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password
            )
            user.phone_number = phone_number
            user.save()
    else:
        form = RegistrationForms()

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)