from .text import TextPropertyType
from lumavate_exceptions import ValidationException
import re

class HtmlEditorPropertyType(TextPropertyType):
  @property
  def type_name(self):
    return 'html-editor'

  