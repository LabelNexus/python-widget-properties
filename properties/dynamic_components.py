from jinja2 import Environment, BaseLoader
from flask import g
from .base_property_type import BasePropertyType
from .dynamic_component import DynamicComponentPropertyType
from lumavate_exceptions import ValidationException

class DynamicComponentsPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'dynamic-components'

  def read(self, data):
    val = data.get(self.property.name, [])
    components = []

    for c in val:
      comp_values = {}

      component_type = c.get('componentType', '__NOTYPE__')
      component_data = c.get('componentData', {})
      component_id = c.get('id', None)
      component_json = next((x for x in self.property.options.get('components', []) if x['type'] == component_type), None)
      if component_json is None:
        raise ValidationException('Invalid Dynamic Component Value: ' + component_type)

      components.append(DynamicComponentPropertyType.get_component_data(component_id, component_type, component_data, component_json))

    self.value = components
    return components
