from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import *
import bcrypt
import re	 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
  return render(request, 'first_app/index.html')

def register(request):
  is_valid=True
  if len(request.POST['fname'])<2: 
    is_valid=False
    messages.error(request, "First name must contain at least two characters.")
  if len(request.POST['lname'])<2:
    is_valid=False
    messages.error(request, "Last name must contain at least two characters.")
  if not EMAIL_REGEX.match(request.POST['email']): 
    is_valid=False 
    messages.error(request, "Invalid email address.")
  if len(request.POST['password'])<8:
    is_valid=False
    messages.error(request, "Password must contain at least 8 characters.")
  if request.POST['password']!=request.POST['cpassword']:
    is_valid=False
    messages.error(request, "Password and password confirmation don't match.")

  if is_valid:
    hashed_pw=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    new_user=Users.objects.create(first_name=request.POST['fname'],last_name=request.POST['lname'], email=request.POST['email'], password=hashed_pw)
    messages.success(request, "You have successfully registered. Please login.")
    print(new_user)
  
  return redirect('/')

def login(request):
  is_valid=True
  if not EMAIL_REGEX.match(request.POST['mail']): 
    is_valid=False 
    messages.error(request, "Invalid email address.")
  if len(request.POST['pwd'])<8:
    is_valid=False
    messages.error(request, "Password must contain at least 8 characters.")

  if is_valid:
    try:
      user=Users.objects.get(email=request.POST['mail'])
      if bcrypt.checkpw(request.POST['pwd'].encode(), user.password.encode()):
        request.session['user_id']=user.id
        return redirect('/quotes')
      else:
        messages.error(request, "Email and password didn't match")
        return redirect('/')

    except Users.DoesNotExist:
      messages.error(request, "A user with this email doesn't exist. Please register.")
      return redirect('/')

  return redirect('/')

def success(request):
  if not 'user_id' in request.session:
    messages.error(request, "You need to login")
    return redirect('/')
  
  else:
    user=Users.objects.get(id=request.session["user_id"])
    all_quotes=Quotes.objects.all()
    context={
      'user':user,
      "quotes":all_quotes,
    }
    print(user.id)
    return render(request, 'first_app/success.html', context)

def logout(request):
  request.session.clear()
  return redirect('/')

def addquote(request):
  is_valid=True
  if len(request.POST['author'])<4: 
    is_valid=False
    messages.error(request, "Author must contain at least three characters.")
  if len(request.POST['quote'])<11:
    is_valid=False
    messages.error(request, "Quote must contain at least ten characters.")

  if is_valid:
    author=request.POST['author']
    quote=request.POST['quote']
    submitted_by=Users.objects.get(id=request.session['user_id'])
    new_quote=Quotes.objects.create(author=author, quote=quote, submitted_by=submitted_by)
    messages.success(request, "You have successfully create a quote.")
    print(new_quote)
  
  return redirect('/quotes')

def deletequote(request, id):
  delete_quote=Quotes.objects.get(id=id)
  delete_quote.delete()
  return redirect('/quotes')

def show(request, id):
  this_account=Users.objects.get(id=id)
  context={
    "id":id,
    "firstname":this_account.first_name,
    "lastname":this_account.last_name,
    "email":this_account.email,
  }
  print(context)
  return render(request, 'first_app/edit.html', context)

def edit(request, id):
  update_account=Users.objects.get(id=id)
  update_account.first_name=request.POST['fname']
  update_account.last_name=last_name=request.POST['lname']
  update_account.email=request.POST['email']
  update_account.save()
  return redirect('/quotes')

def like(request, id):
  this_quote=Quotes.objects.get(id=id)
  this_user=Users.objects.get(id=request.session["user_id"])
  this_quote.liked_by.add(this_user)

  return JsonResponse({'likes_count':this_quote.liked_by.count(),'id':this_quote.id})
  
def quotes(request,id):
  this_user=Users.objects.get(id=id)
  all_quotes=Quotes.objects.filter(submitted_by=id)
  context={
    "id":id,
    "user":this_user,
    "quotes":all_quotes,
  }

  return render(request, 'first_app/quotes.html', context)
