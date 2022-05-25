from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class FontStyleSelectorPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'font-style-selector'

  @property
  def mode(self):
    if self.property.options is None:
      return 'text'

    return self.property.options.get('mode', 'text')

  @property
  def default_font_style(self):
    mode_default = 'h1' if self.mode == 'text' else 'button'
    return self.property.options.get('defaultStyle', mode_default)

  @property
  def default_font_family(self):
    default_value = f'var(--{self.default_font_style}-font-family)'
    if self.property.default is None:
      return default_value

    return self.property.default.get('fontFamily', default_value)

  @property
  def default_font_size(self):
    default_value = f'var(--{self.default_font_style}-font-size)'
    if self.property.default is None:
      return default_value

    return self.property.default.get('fontSize', default_value)

  @property
  def default_font_color(self):
    default_value = f'var(--{self.default_font_style}-font-color)'
    if self.property.default is None:
      return default_value

    return self.property.default.get('fontColor', default_value)


  def read(self, data):
    val = super().read(data)

    if not val:
      val = {}
  
    alignment = val.get('alignment', 'left')
    if alignment not in ['left', 'center', 'right']:
      ValidationException(f'Alignment {alignment} is invalid ', api_field=self.property.name)

    if val.get('fontSize') is None:
      val['fontSize'] = self.default_font_size

    if val.get('fontColor') is None:
      val['fontColor'] = self.default_font_color

    if val.get('fontFamily') is None:
      val['fontFamily'] = self.default_font_family

    if val.get('selectedStyle') is None:
      val['selectedStyle'] = self.default_font_style

    if val.get('bold') is None:
      val['bold'] = self.property.options.get('bold', {}).get('default', False)

    if val.get('italics') is None:
      val['italics'] = self.property.options.get('italics', {}).get('default', False)

    if val.get('alignment') is None:
      val['alignment'] = self.property.options.get('alignment', {}).get('default', 'left')

    return val
