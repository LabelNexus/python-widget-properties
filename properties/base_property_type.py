from ..constants import trigger_read_handlers

class BasePropertyType:
  def __init__(self, property):
    self.property = property

  def read(self, data):
    val = data.get(self.property.name)
    if val is None:
      val = self.property.default

    val = trigger_read_handlers(self.__class__, val)
    return val
