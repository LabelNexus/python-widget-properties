from .base_property_type import BasePropertyType

class ImagePropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'image-upload'
