from django.test import TestCase

import catalog.tests.factories as f
import catalog.models as models
import factory.random as frand


DEF_FACTORY_SEED = 'testing_seed'
BATCH_SIZE = 100


def set_factory_seeds(seed):
    # Set the seed for Factory Boy's random generator
    frand.reseed_random(seed)
    # Set the seed for Faker's random generator
    f.set_faker_seed(seed)


class AuthorModelTest(TestCase):
    LABELS = {'first_name': 'first name',
              'last_name': 'last name',
              'dob': 'dob',
              'dod': 'died'}

    @classmethod
    def setUpTestData(cls):
        set_factory_seeds(DEF_FACTORY_SEED)
        f.AuthorFactory.create_batch(size=10)

    def setUp(self):
        self.author_first = models.Author.objects.first()
        self.authors = models.Author.objects.all()

    def test_labels(self):
        """Verify db fields are properly named"""
        expected = list(self.LABELS.values())
        field_labels = []

        for label in self.LABELS.keys():
            field_labels.append(self.author_first._meta.get_field(label).verbose_name)

        self.assertEqual(expected, field_labels)

    def test_first_name_max_length(self):
        expected = 100
        actual = [author._meta.get_field('first_name').max_length
                              for author in self.authors]

        self.assertTrue(all(ml == expected for ml in actual))

    def test_last_name_max_length(self):
        expected = 100
        actual = [author._meta.get_field('last_name').max_length
                              for author in self.authors]

        self.assertTrue(all(ml == expected for ml in actual))

    def test_str_is_last_comma_first(self):
        expected = [f'{author.last_name}, {author.first_name}'
                    for author in self.authors]
        actual = [f'{str(author)}' for author in self.authors]

        self.assertSequenceEqual(expected, actual)

    def test_absolute_url(self):
        expected = [f'/catalog/authors/{author.id}' for author in self.authors]
        actual = [author.get_absolute_url() for author in self.authors]

        self.assertSequenceEqual(expected, actual)

    def test_dod_after_dob(self):
        actual = [author.dod > author.dob
                  for author in self.authors if author.dod is not None]

        self.assertTrue(False not in actual)


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        set_factory_seeds(DEF_FACTORY_SEED)

        for i in range(BATCH_SIZE):
            gs = f.GenreFactory.create_batch(size=3)
            f.BookFactory.create(post__genre=gs)

    def setUp(self) -> None:
        self.first_book = models.Book.objects.all().first()
        self.books = models.Book.objects.all()

    def test_stuff(self):
        pass