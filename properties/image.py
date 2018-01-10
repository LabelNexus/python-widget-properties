from .base_property_type import BasePropertyType
from .image_base import ImageBase

class ImagePropertyType(BasePropertyType, ImageBase):
  @property
  def type_name(self):
    return 'image-upload'

  def read(self, data):
    val = super().read(data)

    result = self.read_image(val)

    self.value = result
    return result
