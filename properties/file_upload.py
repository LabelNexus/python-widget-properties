from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

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
  def allowed_extensions(self):
    if self.property.options is None:
      return '*'

    return self.property.options.get('allowedExtensions', '*')

  @property
  def allowed_mime_types(self):
    if self.property.options is None:
      return '*'

    return self.property.options.get('allowedMimeTypes', '*')

  def read(self, data):
    val = super().read(data)

    if self.required and not val.get('filename',''):
        raise ValidationException(f'File is required.', api_field=self.property.name)

    if self.allowed_mime_types.strip() != '*':
      mime_types = [t.lower().strip() for t in self.allowed_mime_types.split(',')]
      if val.get('filetype','').lower() not in mime_types:
        raise ValidationException(f'Error Uploading: {val.get("filename","")} - File type is not supported.', api_field=self.property.name)

    return val
