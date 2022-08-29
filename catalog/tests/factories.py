import factory.django as f
from factory import lazy_attribute, post_generation, SubFactory
from faker import Factory

import datetime
from dateutil.relativedelta import relativedelta

from ..models import *


fake = Factory.create()


def set_faker_seed(seed):
    fake.seed(seed)


class AuthorFactory(f.DjangoModelFactory):
    class Meta:
        model = Author
        django_get_or_create = ('first_name', 'last_name', 'dob', 'dod',)

    first_name = lazy_attribute(lambda x: fake.first_name())
    last_name = lazy_attribute(lambda x: fake.last_name())
    dob = lazy_attribute(lambda x: fake.date_of_birth())

    @lazy_attribute
    def dod(self):
        """
        Generate a random date from a range of past and future dates,
          if date in past then DoD assigned, else DoD is NA (author is alive)
        """
        rand_date = fake.date_between(
            start_date=self.dob + relativedelta(years=13),
            end_date=datetime.date(year=2040, month=1, day=1)
        )

        return rand_date if rand_date < datetime.date.today() else None


class GenreFactory(f.DjangoModelFactory):
    class Meta:
        model = Genre
        django_get_or_create = ('name',)

    name = lazy_attribute(
        lambda x: fake.random_element(elements=BOOK_GENRES)
    )


class LanguageFactory(f.DjangoModelFactory):
    class Meta:
        model = Language
        django_get_or_create = ('name',)

    name = lazy_attribute(
        lambda x: fake.random_element(elements=LANGUAGES)
    )


class BookFactory(f.DjangoModelFactory):
    class Meta:
        model = Book
        django_get_or_create = ('isbn',)

    title = lazy_attribute(lambda x: fake.text(max_nb_chars=20))
    author = SubFactory(AuthorFactory)
    summary = lazy_attribute(lambda x: fake.paragraph(nb_sentences=5))
    isbn = lazy_attribute(lambda x: fake.isbn13)
    language = SubFactory(LanguageFactory)

    @post_generation
    def post(self, create, extracted, **kwargs):
        """
        Many-to-many fields require special handling to add to a database;
          django has the 'post_generation' tag which delays binding between
          many-to-many fields and instead requires the passing of desired values
          from the testing methods
        """
        if not create or not kwargs:
            return

        if 'genre' in kwargs:
            for g in kwargs['genre']:
                self.genre.add(g)


class UserUserFactory(f.DjangoModelFactory):
    DEF_PASSWORD = 'P4rol'

    class Meta:
        model = User
        django_get_or_create = ('username',)

    first_name = lazy_attribute(lambda x: fake.first_name())
    last_name = lazy_attribute(lambda x: fake.last_name())
    username = lazy_attribute(lambda x: fake.ascii_safe_email())
    password = DEF_PASSWORD
    groups = ['Library User']

    is_active = True


class UserLibrarianFactory(f.DjangoModelFactory):
    DEF_PASSWORD = 'P4rol'

    class Meta:
        model = User
        django_get_or_create = ('username',)

    first_name = lazy_attribute(lambda x: fake.first_name())
    last_name = lazy_attribute(lambda x: fake.last_name())
    username = lazy_attribute(lambda x: fake.ascii_safe_email())
    password = DEF_PASSWORD
    groups = ['Librarian']

    is_staff = True
    is_active = True


class BookInstanceFactory(f.DjangoModelFactory):
    class Meta:
        model = BookInstance
        django_get_or_create = ('instance_id',)

    instance_id = lazy_attribute(lambda x: fake.uuid4())
    book = SubFactory(BookFactory)
    imprint = lazy_attribute(lambda x: fake.company())
    due_back = lazy_attribute(
        lambda x: fake.date_between(end_date=datetime.date.today() + relativedelta(years=1))
    )
    status = lazy_attribute(
        lambda x: fake.random_element(elements=BookInstance.LOAN_STATUS)
    )

    @post_generation
    def borrower(self, create, extracted, **kwargs):
        if not create or extracted:
            return

        self.borrower.add(extracted)