from jinja2 import Environment, BaseLoader
from flask import g
from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class DynamicComponentsPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'dynamic-components'

  def read(self, data):
#    print(f'Components Property: {self.property.__dict__}\n',flush=True)
    print(f'DCS Property Name: {self.property.name}',flush=True)
#    print(f'Data: {data}\n',flush=True)
    val = super().read(data)
    if val is None:
      val = []
#    print(f'Val: {val}\n',flush=True)

    components = []
    for c in val:
      comp_values = {}

      component_type = c.get('componentType', '__NOTYPE__')
      component_data = c.get('componentData', {})
      component_json = next((x for x in self.property.options.get('components', []) if x['type'] == component_type), None)
      if component_json:
        from ..components import Components
        component = Components.BaseComponent.from_json(component_json)
        component_data = component.read(component_data)

        display_name = component.label
        additional_display = component_data.get('title')
        if additional_display and isinstance(additional_display, dict) and 'en-us' in additional_display:
          display_name = display_name + ' - ' + str(additional_display['en-us'])
        elif additional_display:
          display_name = display_name + ' - ' + str(additional_display)


        result = {
          'componentType': component.component_type,
          'componentData': component_data,
          'displayName': display_name
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

        if display_name_template is None and 'displayNameTemplate' in component_json:
          display_name_template = component_json.get('displayNameTemplate')

        if display_name_template:
          rtemplate = Environment(loader=BaseLoader).from_string(display_name_template)
          result['displayName'] = rtemplate.render(**result)

        components.append(result)
      else:
        raise ValidationException('Invalid Value: ' + component_type)

    self.value = components
    return components
