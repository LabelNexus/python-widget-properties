from flask import request, current_app
from .home_page_type import HomePageTypeComponent
from .base_component import BaseComponent
from ..properties import Properties
import os

class BaseComponent:
  def __init__(self, component_type, category, section, label, display_name, icon_url, properties):
    self.component_type = component_type
    self.category = category
    self.section = section
    self.label = label
    self.display_name = display_name
    self.icon_url = 'a'
    self.properties = properties
    if self.properties is None:
      self.properties = []

  def to_json(self):
    return {
      'type': self.component_type,
      'category': self.category,
      'section': self.section,
      'label': self.label,
      'displayName': self.display_name,
      'icon': self.icon_url,
      'properties': [x.to_json() for x in self.properties]
    }

  @staticmethod
  def from_json(json):
    if json.get('type') == 'home':
      return HomePageTypeComponent()

    else:
      return BaseComponent( \
        json.get('type'), \
        json.get('classification'), \
        json.get('section'), \
        json.get('label'), \
        json.get('display_name'), \
        json.get('icon'), \
        [Properties.Property.from_json(x) for x in json.get('properties', [])])

  def read(self, data):
    result_data = {}
    for x in self.properties:
      result_data[x.name] = x.read(data)

    #if self.component_type == 'location':
    #  result_data.update(behavior.Geocode.GeocodeBehavior().get_coordinates(address=result_data.get('address')))

    return result_data
