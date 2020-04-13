from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User


# Create your views here.
def register(request):
	if request.method == "POST":
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"Account created for {username}! You're now able to login")
			return redirect('login')
	else:
		form = UserRegisterForm()
	
	context = {
	'form' : form
	}
	return render(request, 'users/register.html', context)


@login_required
def profile(request):
	if request.method == "POST":
		u_form = UserUpdateForm(request.POST, instance = request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f"Your profile has been updated!")
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance = request.user)
		p_form = ProfileUpdateForm(instance = request.user.profile)

	context = {
		'u_form' : u_form,
		'p_form' : p_form
	}
	return render(request, 'users/profile.html', context)

def public_profile(request, user_id):
	'''
	Displays public profile for this user id
	'''
	user_object = User.objects.filter(pk = 5).first()
	discussions = user_object.comment_set.all()

	context = {
		'user_object' : user_object,
		'discussions' : discussions
	}

	return render(request, 'users/public_profile.html', context)







