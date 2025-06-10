from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product,Category,Profile
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm
from .forms import UpdateUserForm,ChangePasswordForm,UserChangeForm,PasswordChangeForm,UserInfoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
import json
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html')

def login_user(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            current_user=Profile.objects.get(user__id=request.user.id)
            #get their saved cart from the db
            saved_cart=current_user.old_cart
            if saved_cart:
                #convert to dictionary using json
                converted_cart=json.loads(saved_cart)
                #add the loaded cart dictionary
                cart=Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key,quantity=value)
            messages.success(request,("You have been logged in..."))
            return redirect('home')
        else:
            messages.success(request,("There was an error, Please try again..."))
            return redirect('login')
    else: 
        return render(request,'login.html',{})  

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Account created successfully. You are now logged in.")
            return redirect("home")
        else:
            messages.error(request, "There was an error during registration. Please try again.")
            return redirect("Register")
    return render(request, 'register.html', {'form': form})

def product(request,pk):
    product=Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})

def category(request,foo):
    try:
        
        category= Category.objects.get(name=foo)
        products=Product.objects.filter(category=category)
        return render(request,'category.html',{'products':products,'category':category})

    except:
        messages.success(request,("That category doesn't exist")) 
        return redirect('home')

def category_summary(request):
    categories=Category.objects.all()
    return render(request,'category_summary.html',{"categories":categories})


def update_user(request):
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)
        user_form=UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
           user_form.save()

           login(request,current_user)
           messages.success(request,"User Has Been Updated Successfully...") 
           return redirect('home')
        return render(request,"update_user.html",{'user_form':user_form})
    else:
        messages.success(request,"You must be logged in to access that page...") 
        return redirect('home')
    
#def update_password(request):
    #return render(request,'update_password.html',{})
@login_required
def update_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():  # Corrected to form.is_valid()
            form.save()
            update_session_auth_hash(request, request.user)  # Important to keep the user logged in
            messages.success(request, "Your Password is Successfully Updated.")
            login(request,request.user)
            return redirect('update_user')  # Redirect to login after password change
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)  # Corrected to messages.error()
            return render(request, 'update_password.html', {'form': form})
    else:
        form = ChangePasswordForm(request.user)
        return render(request, 'update_password.html', {'form': form})

def update_info(request):
    if request.user.is_authenticated:
        #current_user=Profile.objects.get(user_id=request.user.id)
        current_user, created = Profile.objects.get_or_create(user__id=request.user.id)
        shipping_user,created=ShippingAddress.objects.get_or_create(user__id=request.user.id)
        form=UserInfoForm(request.POST or None, instance=current_user)

        shipping_form=ShippingForm(request.POST or None,instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
           form.save()
           shipping_form.save()

           
           messages.success(request,"Your info Has Been Updated Successfully...") 
           return redirect('home')
        return render(request,"update_info.html",{'form':form,'shipping_form':shipping_form })
    else:
        messages.success(request,"You must be logged in to access that page...") 
        return redirect('home')
    
def search(request):
    if request.method == "POST":
        query = request.POST.get('searched', '').strip()

        if not query:
            messages.warning(request, "Please enter a search term.")
            return render(request, 'search.html')

        results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

        if not results.exists():
            messages.error(request, "That product does not exist.")
            return render(request, 'search.html', {'searched': []})

        return render(request, 'search.html', {'searched': results})

    return render(request, 'search.html')

    

