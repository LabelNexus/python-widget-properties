
from .base_property_type import BasePropertyType

from flask import g
from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException
from jinja2 import Environment, BaseLoader

class DynamicComponentPropertyType(BasePropertyType):
  @staticmethod
  def options(components):
    #TODO add dynamic flags
    return {
      'components': [x.to_json() for x in components]
    }

  @staticmethod
  def default(component):
    return { 'componentType': component.component_type }

  @property
  def type_name(self):
    return 'dynamic-component'

  def read(self, data):
    val = super().read(data)

    if not isinstance(val, dict):
      raise ValidationException('Invalid Value: ' + str(val))

    component_type = val.get('componentType', '__NOTYPE__')

    # The widget instance could've been created without valid component sets and set to None values.
    # Determine if that is the case and if we should re-evaluate the property
    if component_type == 'None' and self.property.default.get('componentType') is not None:
      val = self.property.default
      component_type = val.get('componentType', '__NOTYPE__')

    component_data = val.get('componentData', {})
    component_json = next((x for x in self.property.options.get('components', []) if x['type'] == component_type), None)

    if component_json:
      from ..components import Components
      component = Components.BaseComponent.from_json(component_json)
      component_data = component.read(component_data)
      result = {
        'componentType': component.component_type,
        'componentData': component_data,
        'displayName': component.component_type
      }

      display_name_template = None
      if component.display_name is not None and '{{' in component.display_name:
        display_name_template = component.display_name

      if component.component_type in g.all_components:
        component_meta = g.all_components.get(component.component_type, {})
        # Flag the component as being used so widget proxy can update component set namespace version table
        component_meta.update({'isUsed': True})

        result['componentTemplate'] = component_meta.get('template', '')
        display_name_template = component_meta.get('displayNameTemplate')

      if display_name_template:
        rtemplate = Environment(loader=BaseLoader).from_string(display_name_template)
        result['displayName'] = rtemplate.render(**result)

    else:
      result = {
        'componentType': 'None',
        'componentData': {},
        'displayName': 'None'
      }

    return result
class DynamicComponentPropertyType(BasePropertyType):
  def __init__(self, tag_type_modifier, classification, section, name, label, property_type_name, options={}, default=None, help_text=None):
    super().__init__(classification, section, name, label, property_type_name, options, default, help_text)
    self.tag_type_modifier = tag_type_modifier

  @property
  def type_name(self):
    return 'dynamic-component'

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
      'tagTypeModifier': self.tag_type_modifier,
      'classification': self.classification,
      'section': self.section,
      'name': self.name,
      'label': self.label,
      'type': self.property_type.type_name,
      'options': self.options,
      'default': self.default,
      'helpText': self.help_text
    }
