from flask import g
from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException
from jinja2 import Environment, BaseLoader

class ComponentPropertyType(BasePropertyType):
  @staticmethod
  def options(components):
    return {
      'categories': [components[0].category],
      'components': [x.to_json() for x in components]
    }

  @staticmethod
  def default(component):
    return { 'componentType': component.component_type }

  @property
  def type_name(self):
    return 'component'

  def read(self, data):
    val = super().read(data)

    if not isinstance(val, dict):
      raise ValidationException('Invalid Value: ' + str(val))

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
      if component.component_type in g.all_components:
        result['componentTemplate'] = g.all_components.get(component.component_type, {}).get('template', '')

    else:
      raise ValidationException('Invalid Value: ' + component_type)

    return result
