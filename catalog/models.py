from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from datetime import date


DEF_CHARFIELD_LENGTH = 200
BOOK_GENRES = ['fiction',
               'science fiction',
               'history',
               'drama',
               'romance',
               'action',
               'suspense',
               'horror',
               'thriller',
               'biography']
LANGUAGES = ['English', 'Russian', 'Korean', 'Spanish', 'Mandarin', 'Cantonese',
             'Ukrainian', 'Italian', 'French', 'Japanese']


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(
        null=True,
        blank=True
    )
    dod = models.DateField(
        'died',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        return reverse('authors-detail', args=[str(self.id)])

    class Meta:
        ordering = ['last_name', 'first_name']
        permissions = (
            ('can_edit_authors', 'Can modify available list of authors'),
        )


class Genre(models.Model):
    name = models.CharField(
        max_length=DEF_CHARFIELD_LENGTH,
        help_text='Enter a book genre (eg. Science Fiction, Biography)'
    )

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(
        max_length=DEF_CHARFIELD_LENGTH,
        help_text='Specify the book\'s language (eg. Russian)'
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(
        max_length=DEF_CHARFIELD_LENGTH
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True
    )
    summary = models.TextField(
        max_length=1000,
        help_text='Enter a brief description of the book'
    )
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        unique=True,
        help_text='13 character unique identification, see: <a href="https://'
                  'www.isbn-international.org/content/what-isbn">ISBN number'
                  '</a>'
    )
    genre = models.ManyToManyField(
        Genre,
        help_text='Select the book\'s genre'
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True
    )

    # Return comma-separated list of genres for list display
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:])

    display_genre.short_description = 'Genre'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    class Meta:
        permissions = (
            ('can_edit_books', 'Can edit available books'),
        )


class BookInstance(models.Model):
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )
    borrower = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    instance_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text='Unique ID for this book in the library'
    )
    book = models.ForeignKey(
        'Book',
        on_delete=models.RESTRICT,
        null=True
    )
    imprint = models.CharField(
        max_length=DEF_CHARFIELD_LENGTH
    )
    due_back = models.DateField(
        null=True,  # Book is not out
        blank=True  # Book reserved indefinitely
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability'
    )

    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)

    def __str__(self):
        return f'{self.instance_id} ({self.book.title})'

    class Meta:
        ordering = ['due_back']
        permissions = (
            ('can_mark_returned_books', 'Can set book as returned'),
            ('can_view_all_books', 'Can view all available book instances'),
        )
