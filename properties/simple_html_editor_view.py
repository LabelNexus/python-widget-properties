from .text import TextPropertyType

class SimpleHtmlEditorViewPropertyType(TextPropertyType):
  @property
  def type_name(self):
    return 'simple-html-editor-view'
