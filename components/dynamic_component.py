from flask import request, current_app
from .base_component import BaseComponent
from ..constants import trigger_read_handlers
from ..properties import Properties
import os

class DynamicComponent(BaseComponent):
  def __init__(self, component_type, section, label, display_name, icon_url, properties, component_set_id, version_id):
    super().__init__(component_type, None, section, label, display_name, icon_url, properties)
    self.component_set_id = component_set_id
    self.component_set_version_id = version_id
    self.icon_url = 'a'
    self.properties = properties
    if self.properties is None:
      self.properties = []

  def to_json(self):
    return {
      'type': self.component_type,
      'section': self.section,
      'label': self.label,
      'displayName': self.display_name,
      'icon': self.icon_url,
      'properties': [x.to_json() for x in self.properties],
      'componentSetId': self.component_set_id,
      'versionId': self.component_set_version_id
    }

  @staticmethod
  def from_json(json):
    return DynamicComponent( \
      json.get('type'), \
      json.get('section'), \
      json.get('label'), \
      json.get('displayName'), \
      json.get('icon'), \
      [Properties.Property.from_json(x) for x in json.get('properties', [])], \
      json.get('componentSetId'), \
      json.get('versionId') \
    )

  def read(self, data):
    result_data = {}
    for prop in self.properties:
      result_data[prop.name] = prop.read(data)

    result_data = trigger_read_handlers(self.__class__, result_data)

    return result_data
