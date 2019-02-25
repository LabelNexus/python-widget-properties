from .text import TextPropertyType
from lumavate_exceptions import ValidationException
import re

class CodeEditorPropertyType(TextPropertyType):
  @property
  def type_name(self):
    return 'code-editor'
