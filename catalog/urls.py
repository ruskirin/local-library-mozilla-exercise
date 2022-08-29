from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreate.as_view(), name='books-create'),
    path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='books-update'),
    path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='books-delete'),
    path('books/<uuid:inst_id>/renew/', views.renew_book_librarian, name='books-renew-librarian'),
    path('books/all/', views.BookListView.as_view(), name='books-all'),
    path('books/all/copies', views.BookInstanceListView.as_view(), name='books-all-copies'),

    path('my/books/', views.UserLoanedBooksListView.as_view(), name='my-books'),

    path('authors/all/', views.AuthorListView.as_view(), name='authors-all'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='authors-detail'),
    path('authors/create/', views.AuthorCreate.as_view(), name='authors-create'),
    path('authors/<int:pk>/update/', views.AuthorUpdate.as_view(), name='authors-update'),
    path('authors/<int:pk>/delete/', views.AuthorDelete.as_view(), name='authors-delete'),
]