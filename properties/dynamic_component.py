from flask import g
from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException
from jinja2 import Environment, BaseLoader

class DynamicComponentPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'dynamic-component'

  def read(self, data):
    val = data.get(self.property.name, {})

    component_type = val.get('componentType', '__NOTYPE__')

    # The widget instance could've been created without valid component sets and set to None values.
    # Determine if that is the case and if we should re-evaluate the property
    if component_type == 'None' and self.property.default is not None and self.property.default.get('componentType') is not None:
      val = self.property.default
      component_type = val.get('componentType', '__NOTYPE__')

    component_id = c.get('id', None)
    component_data = val.get('componentData', {})
    component_json = next((x for x in self.property.options.get('components', []) if x['type'] == component_type), None)
    return DynamicComponentPropertyType.get_component_data(component_id, component_type, component_data, component_json)

  @staticmethod
  def get_component_data(component_id, component_type, component_data, component_json):
    component_def = g.all_components.get(component_type, None)
    if component_def is None:
      return {
        'componentType': 'None',
        'componentData': {},
        'displayName': 'None'
      }

    component_def['id'] = component_id
    component_def['versionId']=component_json.get('versionId')

    from ..components import Components
    component = Components.DynamicComponent.from_json(component_def)
    component_data = component.read(component_data)
    result = {
      'id': component.id,
      'componentType': component.component_type,
      'componentData': component_data,
      'displayName': component.component_type,
      'versionId': component.component_set_version_id,
      'componentSetId': component.component_set_id,
      'icon': component.icon_url
    }

    display_name_template = None
    if component.display_name is not None and '{{' in component.display_name:
      display_name_template = component.display_name

    if component.component_type in g.all_components:
      component_meta = g.all_components.get(component.component_type, {})
      # Flag the component as being used so widget proxy can update component set namespace version table
      component_meta.update({'isUsed': True})

      result['componentTemplate'] = component_def.get('template', '')
      display_name_template = component_def.get('displayNameTemplate')

    if display_name_template:
      rtemplate = Environment(loader=BaseLoader).from_string(display_name_template)
      result['displayName'] = rtemplate.render(**result)

    return result
