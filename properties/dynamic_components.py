from flask import g
from .components import ComponentsPropertyType
from lumavate_exceptions import ValidationException
from jinja2 import Environment, BaseLoader

class DynamicComponentsPropertyType(ComponentsPropertyType):
  @staticmethod
  def options(components):
    print('Dynamic Components options',flush=True)
    jrint('new property type',flush=True)
    return {
      'categories': [components[0].category],
      'components': [x.to_json() for x in components]
    }
  @property
  def type_name(self):
    return 'dynamic-components'
