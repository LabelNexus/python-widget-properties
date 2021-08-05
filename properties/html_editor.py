from .text import TextPropertyType
from lumavate_exceptions import ValidationException
import re

class HtmlEditorPropertyType(TextPropertyType):
  @property
  def type_name(self):
    return 'html-editor'

  def read(self, data):
    val = super().read(data)

    if val is None:
      val = {'en-us': ''}

    elif not isinstance(val, dict):
      val = {'en-us': str(val)}

    return val
