import json
from flask import g
from jinja2 import Environment, BaseLoader
import copy
from .properties import Properties
from .components import Components
from lumavate_signer import ValueHasher
from lumavate_exceptions import ApiException, ValidationException, NotFoundException, InvalidOperationException
from .patch_request import PatchRequest
from .property_signer import PropertySigner

# workaround for sharing between services and platform
try:
  import pyro
except:
  from ._settings import Settings as pyro

class BasePropertyPatcher:
  def __init__(self, version_data, request_json):
    self.patch_request = PatchRequest.from_json(request_json)
    self._request_json = copy.copy(request_json)
    self._version_data = version_data
    self._hasher = ValueHasher(pyro.get_setting('VALUE_HASHER_KEY'))

    self.component_selector_types = ['component', 'dynamic-component']
    self.component_list_types = ['components', 'dynamic-components']

  @classmethod
  def fix_display_name(cls, display_name_value, component_label):
    if display_name_value.lower() == 'id not set' or display_name_value.lower() == 'name not set':
      return component_label

    return display_name_value

  def patch(self):
    delta_data = getattr(self, self.patch_request.operation, lambda: self.default)()
    patched_version_data = self._version_data

    return patched_version_data, delta_data

  def add(self):
    if not self.patch_request.is_component:
      raise ValidationException('Only components can be added')

    if not self.patch_request.is_component or self.patch_request.parent_type not in self.component_list_types:
      raise ValidationException('Invalid operation for property type')

    components = self._get_property_value(self.patch_request.parent_name, [])
    new_component = self._parse_component_data()

    if self.is_component_valid(self.patch_request.component['componentType']):
      component_def = self.get_component_def(self.patch_request.component['componentType'])
      new_component['componentTemplate'] = component_def.get('template', '')
    components.append(new_component)

    return self._create_patch_value('add', self.patch_request.is_component, self.patch_request.parent_name, new_component)

  def copy(self):
    raise ValidationException('Not implemented')

  def get_component_def(self, component_type):
    raise ValidationException('Not implemented')

  def is_component_valid(self, component_type):
    #self.patch_request.component.get('versionId') and component_type)
    return component_type is not None

  def edit(self):
    patch_value = None

    if self.patch_request.is_component:
      component = None
      if self.patch_request.parent_type in self.component_selector_types:
        component = self._get_property_value(self.patch_request.parent_name, {})
      elif self.patch_request.parent_type in self.component_list_types:
        components = self._get_property_value(self.patch_request.parent_name, [])
        component = next((c for c in components if c['id'] == self.patch_request.component_id), None)
      else:
        raise ValidationException('Invalid component type')

      if component is None:
        raise ValidationException('Invalid component')

      new_value = self._read_property_value(self._request_json.get('propertyDef', {}), self.patch_request.property,
                                   self.patch_request.property_value)
      component['componentData'][self.patch_request.property.name] = new_value
      if self.patch_request.parent_type in self.component_list_types:
        component['displayName'] = self._update_display_name(component, new_value)

      custom_result = self._get_custom_component_properties()
      if custom_result is not None:
        new_value = custom_result

      patch_value = {
        'id': component.get('id'),
        'componentData': {self.patch_request.property.name: new_value},
        'displayName': component['displayName']
      }
    else:
      new_value = self._read_property_value(self._request_json.get('propertyDef', {}), self.patch_request.property,
                                   self.patch_request.property_value);
      patch_value = self._set_property_value(self.patch_request.property.name, new_value)

    property_name = self.patch_request.parent_name if self.patch_request.is_component else self.patch_request.property.name
    return self._create_patch_value('edit', self.patch_request.is_component, property_name, patch_value)

  def delete(self):
    if not self.patch_request.is_component or self.patch_request.parent_type not in self.component_list_types:
      raise ValidationException('Invalid operation for property type')

    if self.patch_request.component_id is None:
      raise ValidationException('Invalid component id')

    components = self._get_property_value(self.patch_request.parent_name, [])
    component = next((c for c in components if c['id'] == self.patch_request.component_id), None)
    if component is None:
      raise ValidationException('Invalid component id')

    components.remove(component)
    self._set_property_value(self.patch_request.parent_name, components)

    return self._create_patch_value('delete', True, self.patch_request.parent_name, self.patch_request.component_id)

  def move(self):
    if not self.patch_request.is_component or self.patch_request.parent_type not in self.component_list_types:
      raise ValidationException('Invalid operation for property type')

    if self.patch_request.property_value['sourceIndex'] is None \
        or self.patch_request.property_value['targetIndex'] is None:
      raise ValidationException('Invalid move indices')

    components = self._get_property_value(self.patch_request.parent_name, [])
    source_index = self.patch_request.property_value.get('sourceIndex', -1)
    target_index = self.patch_request.property_value.get('targetIndex', -1)

    if source_index < 0 or target_index < 0 \
        or source_index > len(components) or target_index> len(components):
      raise ValidationException('Index out of range')

    component = components[source_index]

    if component is None or component['id'] != self.patch_request.component_id:
      raise ValidationException('Invalid component id')

    components.insert(target_index, components.pop(source_index))
    self._set_property_value(self.patch_request.parent_name, components)

    patch_value = {
      'sourceIndex': source_index,
      'targetIndex': target_index
    }
    return self._create_patch_value('move', True, self.patch_request.parent_name, patch_value)

  def replace(self):
    if not self.patch_request.is_component or self.patch_request.parent_type not in self.component_selector_types:
      raise ValidationException('Invalid operation for property type')

    patch_value = None
    if self.patch_request.component_type is None:
      patch_value = self._set_property_value(self.patch_request.parent_name, self._get_none_component_type())
    else:
      new_component = self._parse_component_data()
      component_type = self.patch_request.component.get('componentType')
      if component_type is None:
        component_type = self.patch_request.component.get('type')
      if self.is_component_valid(component_type):
        component_def = self.get_component_def(component_type)
        new_component['componentTemplate'] = component_def.get('template', '')
      patch_value = self._set_property_value(self.patch_request.parent_name, new_component)

    return self._create_patch_value('replace', True, self.patch_request.parent_name, patch_value)

  def _create_patch_value(self, operation, is_component, property_name, updated_value):
    return {
      'operation': operation,
      'isComponent': is_component,
      'parentName': self.patch_request.parent_name,
      'parentType': self.patch_request.parent_type,
      'propertyName': property_name,
      'value': updated_value
    }

  def default(self):
    raise ValidationException('Invalid patch operation')

  def _get_property_value(self, property_name, default=None):
    return self._version_data.get(property_name, default)

  def _set_property_value(self, property_name, value):
    self._version_data[property_name] = value
    return { property_name: value }

  """
    Override this for customization components like pageType on a widget
  """
  def _get_custom_component_properties(self):
    return None

  def _get_none_component_type(self):
    return {
      'helpId': None,
      'displayName': None,
      'componentData': {},
      'componentType': None
    }

  # Validates and parses all the component's properties
  def _parse_component_data(self):
    if not self.patch_request.is_component:
      raise ValidationException('Invalid operation for property type')

    future_prop_data = {}
    new_component = self.patch_request.property_value
    component_prop_json = self._request_json.get('componentDef',{}).get('properties', [])
    for prop in self.patch_request.component.get('properties', []):
      prop_json = next((p for p in component_prop_json if p['name'] == prop.name), None)
      future_prop_data[prop.name] = \
        self._read_property_value(prop_json, prop, new_component.get('componentData', {}).get(prop.name, prop.default))

    new_component['componentData'] = future_prop_data

    return self._pack_component(new_component)

  def _pack_component(self, new_component):
    return {
      'id': new_component.get('id'),
      'helpId': new_component.get('helpId',''),
      'componentData': new_component.get('componentData',{}),
      'componentType': new_component.get('componentType'),
      'displayName': new_component.get('displayName'),
      'icon': new_component.get('image',{}).get('preview',''),
      'componentTemplate': new_component.get('componentTemplate','')
      # 'image': new_component['image']
    }

  # Validates the property defintion's signature and then validates and parses the property value
  def _read_property_value(self, property_json, property_def, value):
    self._validate_property_hash(property_json)

    # read property using Property Type validations
    return property_def.read({property_def.name: value})

  def _validate_property_hash(self, prop):
    if prop is None:
      return

    prop_signature = prop.get('signature', None)
    if prop_signature is None:
      raise InvalidOperationException('Invalid property signature')

    if not self._hasher.verify(PropertySigner.filter_signature_properties(prop), bytes(prop_signature, encoding='utf-8')):
      raise InvalidOperationException('Invalid property signature')

  def _update_display_name(self, component, value):
    component_def = self.get_component_def(component['componentType'])

    if component_def is None:
      component_def = self.patch_request.component
      # is a base component, need to get component definition from widget properties
      additional_display = component.get('componentData',{}).get('title')

      display_name = component_def.get('displayName')
      if display_name is None:
        display_name = component_def.get('label','')

      if additional_display and isinstance(additional_display, dict) and 'en-us' in additional_display:
        return '{} - {}'.format(display_name, additional_display['en-us'])
      elif additional_display:
        return '{} - {}'.format(display_name, additional_display)
      else:
        return self.fix_display_name(component['displayName'], component_def.get('label'))

    display_name_template = component_def.get('displayNameTemplate')
    if component['displayName'] is not None and '{{' in component['displayName']:
      display_name_template = component['displayName']

    if display_name_template:
      rtemplate = Environment(loader=BaseLoader).from_string(display_name_template)
      display_name = rtemplate.render(**component)

      return self.fix_display_name(display_name, component_def.get('label'))

