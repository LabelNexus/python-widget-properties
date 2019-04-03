from .base_property_type import BasePropertyType

class TranslatedTextProperty(BasePropertyType):
  @property
  def type_name(self):
    return 'translated-text'

  def read(self, data):
    val = super().read(data)

    if val is None:
      val = {'en-us': ''}

    elif not isinstance(val, dict):
      val = {'en-us': str(val)}

    return val
