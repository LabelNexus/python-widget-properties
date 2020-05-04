
from lumavate_exceptions import ValidationException

class TagModifierPropertyType(BasePropertyType):
  def __init__(self, tag_type_modifier, classification, section, name, label, property_type_name, options={}, default=None, help_text=None):
    super().__init__(classification, section, name, label, property_type_name, options, default, help_text)
    self.tag_type_modifier = tag_type_modifier

  @staticmethod
  def from_json(json):
    if json is None:
      return None

    return Property( \
      json.get('tagTypeModifier'), \
      json.get('classification'), \
      json.get('section'), \
      json.get('name'), \
      json.get('label'), \
      json.get('type'), \
      options=json.get('options'), \
      default=json.get('default'), \
      help_text=json.get('helpText'))

  def to_json(self):
    return {
      'tagTypeModifier': self.tag_type_modifier
      'classification': self.classification,
      'section': self.section,
      'name': self.name,
      'label': self.label,
      'type': self.property_type.type_name,
      'options': self.options,
      'default': self.default,
      'helpText': self.help_text
    }
