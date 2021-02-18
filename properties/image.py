from .base_property_type import BasePropertyType

class ImagePropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'image-upload'

  @property
  def required(self):
    if self.property.options is None:
      return False

    return self.property.options.get('required', False)
