from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class AssetFieldFilterPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'asset-field-filter'
