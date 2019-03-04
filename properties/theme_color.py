from .text import TextPropertyType
from lumavate_exceptions import ValidationException
import re

class ThemeColorPropertyType(TextPropertyType):
  @property
  def type_name(self):
    return 'theme-color'
