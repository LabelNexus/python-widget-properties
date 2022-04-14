from .translated_text import TranslatedTextProperty

from lumavate_exceptions import ValidationException
import re

class HtmlEditorViewPropertyType(TranslatedTextProperty):
  @property
  def type_name(self):
    return 'html-editor-view'
