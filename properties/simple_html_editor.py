from .text import TextPropertyType

class SimpleHtmlEditorPropertyType(TextPropertyType):
  @property
  def type_name(self):
    return 'simple-html-editor'
