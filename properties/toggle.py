from .checkbox import CheckboxPropertyType

class TogglePropertyType(CheckboxPropertyType):
  @property
  def type_name(self):
    return 'toggle'
