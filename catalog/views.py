import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Book, Author, BookInstance, Genre, Language
from .forms import RenewBookForm


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

@login_required
@permission_required('catalog.can_mark_returned_books', raise_exception=True)
def renew_book_librarian(request, inst_id):
    # Verify book instance exists
    book_inst = get_object_or_404(BookInstance, instance_id=inst_id)

    # Check the request type
    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            # Save the cleaned input data
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            # Redirect to a new url
            return HttpResponseRedirect(reverse('books-all-copies'))
    else:
        def_renew_date = datetime.date.today() + datetime.timedelta(weeks=3)

        form = RenewBookForm(initial={'renewal_date': def_renew_date})

    context = {'form': form,
               'book_instance': book_inst}

    return render(request, 'book_renew_librarian.html', context)


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

    permission_required = 'catalog.can_view_all_books'

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
    paginate_by = 5


class AuthorDetailView(generic.DetailView):
    template_name = 'author_detail.html'
    model = Author


class AuthorCreate(PermissionRequiredMixin, CreateView):
    template_name = 'author_edit_form.html'
    permission_required = 'catalog.can_edit_authors'

    model = Author
    fields = ['first_name', 'last_name', 'dob', 'dod']
    initial = {'dod': None}


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'author_edit_form.html'
    permission_required = 'catalog.can_edit_authors'

    model = Author
    fields = ['first_name', 'last_name', 'dob', 'dod']


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'author_delete_form.html'
    permission_required = 'catalog.can_edit_authors'

    model = Author
    success_url = reverse_lazy('authors-all')


class BookCreate(PermissionRequiredMixin, CreateView):
    template_name = 'book_edit_form.html'
    permission_required = 'catalog.can_edit_books'

    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']


class BookUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'book_edit_form.html'
    permission_required = 'catalog.can_edit_books'

    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']


class BookDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'book_delete_form.html'
    permission_required = 'catalog.can_edit_books'

    model = Book
    success_url = reverse_lazy('books-all')