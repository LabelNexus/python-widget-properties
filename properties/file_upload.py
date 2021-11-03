from .base_property_type import BasePropertyType

class FileUploadPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'file-upload'

  @property
  def required(self):
    if self.property.options is None:
      return False

    return self.property.options.get('required', False)

  @property
  def allowed_file_types(self):
    if self.property.options is None:
      return '*'

    return self.property.options.get('allowedTypes', '*')
