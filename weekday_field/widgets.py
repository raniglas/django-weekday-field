from django import forms
from .utils import BITWISE_DAY_CHOICES

class BitwiseWeekdaySelect(forms.widgets.SelectMultiple):
  def __init__(self, *args, **kwargs):
    if 'choices' not in kwargs:
      kwargs['choices'] = [(x[0],x[2]) for x in BITWISE_DAY_CHOICES]

    super(BitwiseWeekdaySelect, self).__init__(*args, **kwargs)

