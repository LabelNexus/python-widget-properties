from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class FontStylePropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'font-style'

  @property
  def default_font_family(self):
    if self.property.default is None:
      return 'primary'

    return self.property.default.get('fontFamily', 'primary')

  @property
  def default_font_size(self):
    if self.property.default is None:
      return 16

    return self.property.default.get('fontSize', 16)

  @property
  def default_font_color(self):
    if self.property.default is None:
      return 'var(--primary-color)'

    return self.property.default.get('fontColor', 'var(--primary-color)')

  @property
  def include_underline(self):
    if self.property.options is None:
      return False

    return self.property.options.get('includeUnderline', False)


  def read(self, data):
    val = super().read(data)

    if not val.get('fontSize'):
      val['fontSize'] = self.default_font_size

    if not val.get('fontColor'):
      val['fontColor'] = self.default_font_color

    if not val.get('fontFamily'):
      val['fontFamily'] = self.default_font_family

    return val

