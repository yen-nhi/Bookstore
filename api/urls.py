from django.urls import path
from . import views

urlpatterns = [
    path('create-book/', views.createBook, name='create-book'),
    path('get-books', views.getBooks, name='get-all-books'),
    path('get-book/<int:book_id>/', views.getBookById, name='get-book-by-ID'),
    path('update-book/<int:book_id>/', views.updateBook, name='update-book'),
    path('delete-book/<int:book_id>/', views.deleteBook, name='delete-book-by-ID'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),

]
