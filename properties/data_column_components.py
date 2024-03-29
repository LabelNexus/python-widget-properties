from jinja2 import Environment, BaseLoader
from flask import g
from .components import ComponentsPropertyType
from lumavate_exceptions import ValidationException

class DataColumnComponentsPropertyType(ComponentsPropertyType):
  @staticmethod
  def options(components, is_primary=False):
    return {
      'categories': [components[0].category] if len(components) > 0 else [],
      'components': [x.to_json() for x in components],
      'isPrimary': is_primary
    }

  @staticmethod
  def default(component):
    return { 'componentType': component.component_type }

  @property
  def type_name(self):
    return 'data-column-components'

  def read(self, data):
    if not g.get('all_components'):
      g.all_components = {}

    return super().read(data)
