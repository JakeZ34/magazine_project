from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def magazines(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'all_magazines': Magazine.objects.all(),
            'active_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'magazines.html', context)

def sign_up(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validator(request.POST)
    if errors:
        for i in errors.values():
            messages.error(request, i)
        return redirect('/')
    else:
        new_user = User.objects.sign_up(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "Sign up successful")
        return redirect('/magazines')

def sign_in(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticator(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid credentials')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "Log in successful")
    return redirect('/magazines')

def create_magazine(request):
    errors = Magazine.objects.mag_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/magazines')
    else:
        user = User.objects.get(id=request.session['user_id'])
        magazine = Magazine.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            creator = user
        )
    user.favorited_magazines.add(magazine)
    return redirect(f'/magazines/{magazine.id}')

def show_mag(request, magazine_id):
    context = {
        'magazine': Magazine.objects.get(id=magazine_id),
        'active_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "show_magazine.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

def delete(request, magazine_id):
    magazine = Magazine.objects.get(id=magazine_id)
    magazine.delete()
    return redirect('/magazines')


def update(request, magazine_id):
    errors = Magazine.objects.mag_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/magazines')
    else:
        magazine = Magazine.objects.get(id=magazine_id)
        magazine.description = request.POST['description']
        magazine.title = request.POST['title']
        magazine.save()
    return redirect(f"/magazines/{magazine_id}")

def favorite(request, magazine_id):
    user = User.objects.get(id=request.session["user_id"])
    magazine = Magazine.objects.get(id=magazine_id)
    user.favorited_magazines.add(magazine)

    return redirect(f"/magazines/{magazine_id}")

def unfavorite(request, magazine_id):
    user = User.objects.get(id=request.session["user_id"])
    magazine = Magazine.objects.get(id=magazine_id)
    user.favorited_magazines.remove(magazine)

    return redirect(f"/magazines/{magazine_id}")

def back(request):
    return redirect('/magazines')
