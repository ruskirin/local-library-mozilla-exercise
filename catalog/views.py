import datetime
from django.shortcuts import render, get_object_or_404
from django.views import generic
# from catalog.forms import RenewBookForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Book, Author, BookInstance, Genre, Language


def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    num_books = Book.objects.all().count()
    languages = list(Language.objects.all().values_list('name', flat=True))
    genres = list(Genre.objects.all().values_list('name', flat=True))
    num_authors = Author.objects.all().count()
    num_author_rinat = Author.objects\
        .filter(first_name__iexact='rinat',
                last_name__iexact='ibragimov')\
        .count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance\
        .objects.filter(status__exact='a').count()

    # A dictionary mapping above variables to names
    context = {
        'num_visits': num_visits,
        'num_books': num_books,
        'num_languages': languages,
        'num_genres': genres,
        'num_authors': num_authors,
        'num_author_rinat': num_author_rinat,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
    }

    return render(request, 'index.html', context=context)


def renew_book_librarian(request, inst_id):
    # Verify book instance exists
    bookinst = get_object_or_404(BookInstance, inst_id)

    # Check the request type
    if request.method == 'POST':
        form = # RenewBookForm(request.POST)
    else:



class UserLoanedBooksListView(LoginRequiredMixin, generic.ListView):
    template_name = 'bookinstance_user_borrowed_list.html'
    model = BookInstance
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects\
            .filter(borrower=self.request.user)\
            .filter(status__exact='o')\
            .order_by('due_back')


class BookInstanceListView(PermissionRequiredMixin, generic.ListView):
    template_name = 'bookinstance_list.html'
    model = BookInstance
    context_object_name = 'instance_list'
    paginate_by = 2

    permission_required = 'catalog.can_view_all'

    def get_queryset(self):
        return BookInstance.objects.all()


class BookListView(generic.ListView):
    template_name = 'book_list.html'
    model = Book
    context_object_name = 'book_list'
    paginate_by = 2


class BookDetailView(generic.DetailView):
    template_name = 'book_detail.html'
    model = Book


class AuthorListView(generic.ListView):
    template_name = 'author_list.html'
    model = Author
    context_object_name = 'author_list'
    paginate_by = 1


class AuthorDetailView(generic.DetailView):
    template_name = 'author_detail.html'
    model = Author