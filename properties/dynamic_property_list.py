
from jinja2 import Environment, BaseLoader
from flask import g
from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class DynamicPropertyListPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'dynamic-property-list'

  @property
  def property_def(self):
    # avoid circular reference
    from .property import Property

    if self.property.options is None or self.property.options.get('propertyDef') is None:
      raise ValidationException(f'Missing Options. Options with key "propertyDef" is required', api_field=self.property.name)

    property_def = self.property.options.get('propertyDef')
    return Property.from_json(property_def.get('type'))

  def read(self, data):
    val = data.get(self.property.name, [])
    if val is None:
      val = []
    properties = []

    # TODO: Get property type from property.get_property_type for  property_def
    # TODO: read each item in array using that property type and its validations,
    property_def = self.property_def
    # return the list of parsed properties

    """
    for p in val:
      comp_values = {}

      component_type = c.get('componentType', '__NOTYPE__')
      component_data = c.get('componentData', {})
      component_id = c.get('id', None)
      component_json = next((x for x in self.property.options.get('components', []) if x['type'] == component_type), None)
      if component_json is None:
        raise ValidationException('Invalid Dynamic Component Value: ' + component_type)

      components.append(DynamicComponentPropertyType.get_component_data(component_id, component_type, component_data, component_json))

    self.value = components
    """
    return properties
