import behavior

class Property:
  def __init__(self, classification, section, name, label, property_type_name, options={}, default=None):
    self.property_type = self.get_property_type(property_type_name)
    self.classification = classification
    self.section = section
    self.name = name
    self.label = label
    self.default = default
    self.property_type.property = self
    self.options = options

  @staticmethod
  def from_json(json):
    return Property( \
      json.get('classification'), \
      json.get('section'), \
      json.get('name'), \
      json.get('label'), \
      json.get('type'), \
      options=json.get('options'), \
      default=json.get('default'))

  def get_property_type(self, type_name):
    types = {
      'text' : behavior.Properties.TextPropertyType,
      'color': behavior.Properties.ColorPropertyType,
      'image-upload': behavior.Properties.ImagePropertyType,
      'component': behavior.Properties.ComponentPropertyType,
      'components': behavior.Properties.ComponentsPropertyType,
      'checkbox': behavior.Properties.CheckboxPropertyType,
      'toggle': behavior.Properties.TogglePropertyType,
      'translated-text': behavior.Properties.TranslatedTextProperty,
      'dropdown': behavior.Properties.DropdownPropertyType,
      'multiselect': behavior.Properties.MultiselectPropertyType,
      'numeric': behavior.Properties.NumericPropertyType,
      'model-image-upload': behavior.Properties.ModelImagePropertyType,
      'header-title': behavior.Properties.HeaderTitlePropertyiType,
      'page-link': behavior.Properties.PageLinkPropertyType
    }

    prop_type = types.get(type_name)
    if prop_type is None:
      raise Exception('Unknown type name')

    return prop_type(self)

  def to_json(self):
    return {
      'classification': self.classification,
      'section': self.section,
      'name': self.name,
      'label': self.label,
      'type': self.property_type.type_name,
      'options': self.options,
      'default': self.default
    }

  def read(self, data):
    return self.property_type.read(data)
