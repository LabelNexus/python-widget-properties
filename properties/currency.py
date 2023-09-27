from .numeric import NumericPropertyType 
from lumavate_exceptions import ValidationException

class CurrencyPropertyType(NumericPropertyType):
  @property
  def type_name(self):
    return 'currency'

  def allow_empty(self):
    return True


