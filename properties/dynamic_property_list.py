
from jinja2 import Environment, BaseLoader
from flask import g
from .base_property_type import BasePropertyType
from .dynamic_component import DynamicComponentPropertyType
from lumavate_exceptions import ValidationException
import copy

class DynamicPropertyListPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'dynamic-property-list'

  @property
  def property_def(self):
    # avoid circular reference
    from .property import Property

    if self.property.options is None or self.property.options.get('propertyDef') is None:
      raise ValidationException(f'Missing options key, "propertyDef", is required', api_field=self.property.name)

    property_def_json = self.property.options.get('propertyDef')
    return Property.from_json(property_def_json)

  @property
  def save_incomplete_data(self):
    return self.property.options.get('saveIncompleteData',True)

  def read(self, data):
    val = data.get(self.property.name, [])
    if val is None:
      val = []
    
    parsed_values = []

    base_property_def = self.property_def
    if isinstance(val, dict) and 'dataColumnRef' in val:
      return val

    for prop_value in val:
      if base_property_def.property_type.type_name == 'dynamic-component':
        for key,value in prop_value.items():
          if not value:
            parsed_values.append({key: value})
            continue

          component_type = value.get('componentType', '__NOTYPE__')
          component_data = value.get('componentData', {})
          component_id = value.get('id', None)
          component_json = g.all_components.get(component_type, None)
          if component_json is None:
            raise ValidationException('Invalid Child Component Value: ' + component_type)

          parsed_values.append({key: DynamicComponentPropertyType.get_component_data(component_id, component_type, component_data, component_json)})

      elif isinstance(prop_value, dict):
        for key,value in prop_value.items():
          if not self.save_incomplete_data and (value is None or self._is_empty_asset_ref(value)):
            continue

          property_def_instance = self._get_property_instance(base_property_def, key, value)
          parsed_values.append({key: property_def_instance.read(prop_value)});

    return parsed_values

  # base_property_def needs to be converted to a unique property definition
  # since each property value will have a unique name and value
  def _get_property_instance(self, base_property_def, key, value):
    property_def_instance = copy.deepcopy(base_property_def)
    property_def_instance.name = key
    return property_def_instance


  def _is_empty_asset_ref(self,value):
    return not value or (type(value) is dict and 'assetRef' in value and not value['assetRef']['assetId'])
