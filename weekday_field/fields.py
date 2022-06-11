from django.db import models
from django.core.validators import validate_comma_separated_integer_list

from .forms import WeekdayFormField, BitwiseWeekdayFormField

def validate_csv(data):
    return all(map(lambda x:isinstance(x, int), data))
    
class WeekdayField(models.CharField):
    """
    Field to simplify the handling of a multiple choice of None->all days.
    
    Stores as CSInt.
    """
    description = "CSV Weekday Field"
    default_validators = [validate_csv]
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 14
        super(WeekdayField, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        return super(WeekdayField, self).formfield(form_class=WeekdayFormField, **kwargs)
    
    def from_db_value(self, value, expression, connection, context):
        try:
            basestring
        except NameError:
            basestring = str

        if isinstance(value, str):
            if value:
                value = [int(x) for x in value.strip('[]').split(',') if x]
            else:
                value = []

        return value
    
    def get_db_prep_value(self, value, connection=None, prepared=False):
        return ",".join([str(x) for x in value])

    def to_python(self, value):
        try:
            basestring
        except NameError:
            basestring = str
        if isinstance(value, str):
            if value:
                value = [int(x) for x in value.strip('[]').split(',') if x]
            else:
                value = []
        return value

        
def validate_bitwise_notation(data):
  return data > 0 and data <= (2**7 - 1)

class BitwiseWeekdayField(models.IntegerField):
  description = "Bitwise Weekday Field"
  default_validators = [validate_bitwise_notation]

  def to_python(self, value):
    if isinstance(value, int):
      return BitwiseDays(value)
    return value

  def formfield(self, **kwargs):
    return super(BitwiseWeekdayField, self).formfield(form_class=BitwiseWeekdayFormField, **kwargs)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^weekday_field\.fields\.WeekdayField'])
    add_introspection_rules([], ['^weekday_field\.fields\.BitwiseWeekdayField'])
except ImportError:
    pass
