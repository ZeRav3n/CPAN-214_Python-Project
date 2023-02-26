from atexit import register
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BookForm
from .models import Book
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            print('User does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            print('Invalid username or passwors')
    context = {'page': page}
    return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/')

def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('/')
        else:
            print("Error in registration")
    return render(request, 'login_register.html', {'form': form})

def books(request):
    books = Book.objects.all()
    context = {"page_title": "Books", 'books': books}
    return render(request, 'homepage.html', context)

def book(request, pk):
    book = Book.objects.get(id=pk)
    context = {"page_title": "Books", 'books': books}
    return render(request, 'book.html', context)

@login_required(login_url='login')
def addBook(request):
    form = BookForm()
    if request.method == 'POST':
        Book.objects.create(
            title = request.POST.get('title'),
            author = request.POST.get('author'),
            description = request.POST.get('description'),
            rating = request.POST.get('rating'),
            posted_by = request.user
        )
        return redirect('/')
    context = {'form': form}
    return render(request, 'book_form.html', context)

@login_required(login_url='login')
def updateBook(request, pk):
    book = Book.objects.get(id=pk)
    form = BookForm(instance=book)
    if request.user != book.posted_by:
        return render(request, 'unauthorized.html')
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.description = request.POST.get('description')
        book.rating = request.POST.get('rating')
        book.save()
        return redirect('/')
    context = {'form': form, 'book': book}
    return render(request, 'book_form.html', context)

@login_required(login_url='login')
def deleteBook(request, pk):
    book = Book.objects.get(id=pk)
    if request.user != book.posted_by:
        return render(request, 'unauthorized.html')
    if request.method == 'POST':
        book.delete()
        return redirect('/')
    return render(request, 'delete.html', {'obj': book})