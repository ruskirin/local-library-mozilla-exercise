import re
from math import ceil

import factory.random as frand
from django.test import TestCase
from django.urls import reverse

from catalog.tests.factories import AuthorFactory
from catalog.models import Author


class AuthorListViewTest(TestCase):
    FACTORY_SEED = 'testing_seed'
    BATCH_SIZE = 100
    PAGINATE_BY = 5

    @classmethod
    def setUpTestData(cls):
        frand.reseed_random(cls.FACTORY_SEED)
        AuthorFactory.set_faker_seed(cls.FACTORY_SEED)

        AuthorFactory.create_batch(size=cls.BATCH_SIZE)

    def setUp(self):
        self.paginate_by = self.PAGINATE_BY

    def test_view_url_at_specified(self):
        url = '/catalog/authors/all/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_view_name_reverse_url(self):
        url_name = 'authors-all'

        response = self.client.get(reverse(url_name))
        self.assertEqual(response.status_code, 200)

    def test_view_correct_template(self):
        template = 'author_list.html'

        response = self.client.get(reverse('authors-all'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, template)

    # def test_context(self):
    #     response = self.client.get(reverse('authors-all'))
    #     print(f'* context: {response.context}')
    #
    #     return True

    def test_paginate_by(self):
        response = self.client.get(reverse('authors-all'))
        self.assertEqual(response.status_code, 200)

        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)

        self.assertEqual(len(response.context['author_list']), self.PAGINATE_BY)

        last_page_actual = response.context['paginator'].num_pages
        last_page_expected = ceil(self.BATCH_SIZE/self.PAGINATE_BY)

        self.assertEqual(last_page_actual, last_page_expected)

    def test_list_all_authors_shown(self):
        response = self.client.get(reverse('authors-all'))
        self.assertEqual(response.status_code, 200)

