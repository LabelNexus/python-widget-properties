from flask import request, current_app
from ..constants import trigger_read_handlers
from ..properties import Properties
import os

class BaseComponent:
  def __init__(self, component_type, category, section, label, display_name, icon_url, properties, help_id=None, display_name_template=None, position='right'):
    self.component_type = component_type
    self.category = category
    self.section = section
    self.label = label
    self.display_name = display_name if display_name else label
    self.display_name_template = display_name_template
    self.icon_url = 'a' if icon_url is None else icon_url
    self.properties = properties
    if self.properties is None:
      self.properties = []

    self.help_id = help_id
    self.position = position
    self.component_set_id = None
    self.component_set_version_id = None

  def to_json(self):
    return {
      'type': self.component_type,
      'category': self.category,
      'section': self.section,
      'label': self.label,
      'displayName': self.display_name if self.display_name else self.label,
      'displayNameTemplate': self.display_name_template,
      'icon': self.icon_url,
      'properties': [x.to_json() for x in self.properties],
      'helpId': self.help_id,
      'position': self.position
    }

  @staticmethod
  def from_json(json):
    if json.get('type') == 'home':
      from .home_page_type import HomePageTypeComponent
      return HomePageTypeComponent()

    else:
      return BaseComponent( \
        json.get('type'), \
        json.get('classification'), \
        json.get('section'), \
        json.get('label'), \
        json.get('displayName'), \
        json.get('icon'), \
        [Properties.Property.from_json(x) for x in json.get('properties', [])], \
        json.get('helpId'), \
        json.get('displayNameTemplate'), \
        position = json.get('position'))

  def read(self, data):
    result_data = {}
    for x in self.properties:
      result_data[x.name] = x.read(data)

    result_data = trigger_read_handlers(self.__class__, result_data)

    #if self.component_type == 'location':
    #  result_data.update(behavior.Geocode.GeocodeBehavior().get_coordinates(address=result_data.get('address')))

    return result_data
