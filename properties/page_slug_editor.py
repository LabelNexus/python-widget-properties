from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class PageSlugEditorPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'page-slug-editor'
