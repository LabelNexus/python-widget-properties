from .translated_text import TranslatedTextProperty

from lumavate_exceptions import ValidationException
import re

class HtmlEditorPropertyType(TranslatedTextProperty):
  @property
  def type_name(self):
    return 'html-editor'
