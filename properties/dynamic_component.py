from flask import g
from .component import ComponentPropertyType
from lumavate_exceptions import ValidationException
from jinja2 import Environment, BaseLoader

class DynamicComponentPropertyType(ComponentPropertyType):
  @staticmethod
  def options(components):
    print('Dynamic Component options',flush=True)
    return {
      'categories': [components[0].category],
      'components': [x.to_json() for x in components]
    }
  @property
  def type_name(self):
    return 'dynamic-component'
