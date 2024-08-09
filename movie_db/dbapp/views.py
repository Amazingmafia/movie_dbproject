from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm, MovieForm
from .models import Movie, Genre
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from django.db.models import Q
from django.core.mail import send_mail

def home(request):
    movies = Movie.objects.all()
    return render(request, 'home.html', {'movies': movies})

def search(request):
    query = request.GET.get('query', '')
    genre_id = request.GET.get('genre', '')

    # Filter by genre if provided
    if genre_id:
        genre = get_object_or_404(Genre, id=genre_id)
        movies = Movie.objects.filter(title__icontains=query, genre=genre)
    else:
        movies = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(genre__name__icontains=query)
        )

    return render(request, 'search_results.html', {'movies': movies, 'query': query})

def movies_by_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    movies = Movie.objects.filter(genre=genre)
    return render(request, 'movies_by_genre.html', {'genre': genre, 'movies': movies})

@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movie_details', movie_id=movie.id)
    else:
        form = ReviewForm()

    return render(request, 'movie_details.html', {'movie': movie, 'review_form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            # Create the user
            user = User.objects.create_user(username=username, password=password, email=email)

            # Log the user in
            auth_login(request, user)

            # Email content
            subject = 'Welcome to Movie Site!'
            message = f'Hi {username},\n\nThank you for registering at Movie Site. We are excited to have you on board!'
            recipient_list = [email]

            # Send email
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )

            # Redirect to home page
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            return redirect('home')
        else:
            print("Form errors:", form.errors)

    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form})

def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if movie.added_by != request.user:
        return redirect('home')  # Redirect if the user is not the one who uploaded the movie

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_details', movie_id=movie.id)
    else:
        form = MovieForm(instance=movie)

    return render(request, 'edit_movie.html', {'form': form, 'movie': movie})

@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if movie.added_by == request.user:
        movie.delete()
    return redirect('home')

def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movie_details.html', {'movie': movie})

def admin(request):
    return render(request, 'admin.html')

def logout(request):
    auth_logout(request)
    return redirect('home')
