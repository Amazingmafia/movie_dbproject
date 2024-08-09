from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('genre/<int:genre_id>/', views.movies_by_genre, name='movies_by_genre'),
    path('add_review/<int:movie_id>/', views.add_review, name='add_review'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('edit_movie/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('delete_movie/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('movie_details/<int:movie_id>/', views.movie_details, name='movie_details'),
    path('admin/', views.admin, name='admin'),
    path('logout/', views.logout, name='logout'),
]

#     path('', views.home, name='home'),
#     path('login/', views.login, name='login'),
#     path('register/', views.register, name='register'),
#     path('add-movie/', views.add_movie, name='add_movie'),
#     path('movie-details/<int:movie_id>/', views.movie_details, name='movie_details'),
#     path('delete-movie/<int:movie_id>/', views.delete_movie, name='delete_movie'),
#     path('edit-movie/<int:movie_id>/', views.edit_movie, name='edit_movie'),
#     path('add-review/<int:movie_id>/', views.add_review, name='add_review'),
#     path('movies_by_genre/<int:genre_id>/', views.movies_by_genre, name='movies_by_genre'),
#     path('search/', views.search, name='search'),
#     path('logout/', views.logout, name='logout'),
#     path('admin/', views.admin, name='admin'),
# ]
