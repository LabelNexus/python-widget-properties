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

  @property
  def max_file_size(self):
    if self.property.options is None:
      return None

    size = self.property.options.get('maxFileSize')
    if size is not None:
      return int(size)

  def read(self, data):
    val = super().read(data)
    print(f'VAL: {val}',flush=True)

    if self.required and not val.get('filename',''):
        raise ValidationException(f'File is required.', api_field=self.property.name)

    if self.allowed_extensions.strip() != '*':
      extensions = [t.lower().strip() for t in self.allowed_extensions.split(',')]
      if val.get('extension','').lower() not in extensions:
        raise ValidationException(f'File extension: {val.get("extension")} is not supported.', api_field=self.property.name)

    if self.allowed_mime_types.strip() != '*':
      mime_types = [t.lower().strip() for t in self.allowed_mime_types.split(',')]
      if val.get('filetype','').lower() not in mime_types:
        raise ValidationException(f'File type: {val.get("filetype")} is not supported.', api_field=self.property.name)

    if self.max_file_size is not None and  val.get('size') > self.max_file_size:
      raise ValidationException(f'File is too large.', api_field=self.property.name)

    return val
