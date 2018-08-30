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

      if component.component_type in g.all_components:
        result['componentTemplate'] = g.all_components.get(component.component_type, {}).get('template', '')
        display_name_template = g.all_components.get(component.component_type, {}).get('displayNameTemplate')

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
