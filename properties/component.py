from flask import g
from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException
from jinja2 import Environment, BaseLoader

class ComponentPropertyType(BasePropertyType):
  @staticmethod
  def options(components, isRequired=False, base_options={}):
    base_options.update({
      'categories': [components[0].category],
      'components': [x.to_json() for x in components],
      'isRequired': isRequired
    })
    
    return base_options

  @staticmethod
  def default(component, data={}):
    default_data = {}
    default_data[component.component_type] = data
    return { 'componentType': component.component_type, 'componentData': default_data }

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
      component = None
      if component_type == 'home':
        component = Components.BaseComponent.from_json(component_json)
      else:
        component = Components.DynamicComponent.from_json(component_json)

      component_data = component.read(component_data)

      result = {
        'id': val.get('id'),
        'componentType': val.get('componentType'),
        'componentData': component_data,
        'displayName': val.get('componentType'),
        'versionId': val.get('versionId', component.component_set_version_id),
        'componentSetId': val.get('componentSetId', component.component_set_id),
        'icon': component.icon_url,
        'helpId': component.help_id
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
        'displayName': 'None',
        'helpId': 'None'
      }

    return result
