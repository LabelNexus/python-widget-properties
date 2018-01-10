class BasePropertyType:
  def __init__(self, property):
    self.property = property

  def read(self, data):
    val = data.get(self.property.name)
    if val is None:
      val = self.property.default

    return val
