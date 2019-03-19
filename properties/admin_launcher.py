from .text import TextPropertyType

class AdminLauncherPropertyType(TextPropertyType):
  @property
  def type_name(self):
    return 'admin-launcher'
