from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class PageLinkPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'page-link'
