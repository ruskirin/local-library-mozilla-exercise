import datetime

from django.test import SimpleTestCase

from catalog.forms import RenewBookForm


class RenewBookFormTest(SimpleTestCase):
    LABELS = {
        'due_back': 'New renewal date'
    }

    def setUp(self):
        self.form = RenewBookForm()

    def test_due_back_form_label(self):
        expected = self.LABELS['due_back']
        fl = self.form.fields['due_back'].label

        print(expected, fl)

        # If label is not explicitly set, defaults to None
        self.assertTrue((fl is None) or (fl == expected))

    def test_due_back_form_help_text(self):
        expected = 'Choose a date within the next 4 weeks (default: 3 weeks)'
        help_text = self.form.fields['due_back'].help_text

        self.assertEqual(expected, help_text)

    def test_due_back_date_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        self.form = RenewBookForm(data={'due_back': date})

        self.assertFalse(self.form.is_valid())

    def test_due_back_date_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4, days=1)
        self.form = RenewBookForm(data={'due_back': date})

        self.assertFalse(self.form.is_valid())

    def test_due_back_date_today(self):
        date = datetime.date.today()
        self.form = RenewBookForm(data={'due_back': date})

        self.assertTrue(self.form.is_valid())

    def test_due_back_date_max(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4)
        self.form = RenewBookForm(data={'due_back': date})

        self.assertTrue(self.form.is_valid())