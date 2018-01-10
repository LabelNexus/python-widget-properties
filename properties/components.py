from .base_property_type import BasePropertyType
from ..exceptions import ValidationException
import behavior

class ComponentsPropertyType(BasePropertyType):
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
    return 'components'

  def read(self, data):
    val = super().read(data)

    components = []
    for c in val:
      comp_values = {}

      component_type = c.get('componentType', '__NOTYPE__')
      component_data = c.get('componentData', {})
      component_json = next((x for x in self.property.options.get('components', []) if x['type'] == component_type), None)
      if component_json:
        component = behavior.Components.BaseComponent.from_json(component_json)
        component_data = component.read(component_data)
        additional_display = component_data.get('title', {}).get('en-us')
        if additional_display:
          additional_display = ' - ' + str(additional_display)
        else:
          additional_display = ''

        result = {
          'componentType': component.component_type,
          'componentData': component_data,
          'displayName': component.label + additional_display
        }
        components.append(result)
      else:
        raise ValidationException('Invalid Value: ' + component_type)

    self.value = components
    return components
