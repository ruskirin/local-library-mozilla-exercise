import datetime

from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import BookInstance


class RenewBookForm(ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise ValidationError(_('Cannot renew into the past'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Cannot renew to more than 4 weeks'))

        return data

    class Meta:
        model = BookInstance

        fields = ['due_back']
        labels = {'due_back': _('New renewal date')}
        help_texts = {'due_back': _('Choose a date within the next 4 weeks '
                                    '(default: 3 weeks)')}