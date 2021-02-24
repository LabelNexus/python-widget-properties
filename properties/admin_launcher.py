from .base_property_type import BasePropertyType

class AdminLauncherPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'admin-launcher'
