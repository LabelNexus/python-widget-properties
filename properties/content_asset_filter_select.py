from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class ContentAssetFilterSelectPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'content-asset-filter-select'
