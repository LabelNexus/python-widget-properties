from .base_property_type import BasePropertyType

class MultiselectPropertyType(BasePropertyType):
  @staticmethod
  def options(options):
    if options is None:
      return []

    return options

  @staticmethod
  def default(options):
    if options is None:
      return []

    return [x['value'] for x in options]

  @property
  def type_name(self):
    return 'multiselect'

  def read(self, data):
    val = super().read(data)

    check_hash = { str(x['value']): x['value'] for x in self.property.options }
    check_hash['None'] = None

    if val is None:
      val = self.property.default

    val = [check_hash[str(x)] for x in val if check_hash.get(str(x))]

    return val
