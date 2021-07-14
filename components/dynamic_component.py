from flask import request, current_app
import uuid
from .base_component import BaseComponent
from ..constants import trigger_read_handlers
from ..properties import Properties
import os

class DynamicComponent(BaseComponent):
  def __init__(self, id, component_type, section, label, display_name, display_name_template, icon_url, properties, help_id, component_set_id, version_id, position='right',
      tag_modifiers=True):
    super().__init__(component_type, None, section, label, display_name, icon_url, properties, help_id, display_name_template, position=position,
        tag_modifiers=tag_modifiers)
    # This is used on the client for updating a component, just keep it as a string
    self.id = id if id is not None else str(uuid.uuid4())

    self.component_set_id = component_set_id
    self.component_set_version_id = version_id

  def to_json(self):
    return {
      'id': self.id,
      'type': self.component_type,
      'section': self.section,
      'label': self.label,
      'displayName': self.display_name if self.display_name else self.label,
      'displayNameTemplate': self.display_name_template,
      'icon': self.icon_url,
      'properties': [x.to_json() for x in self.properties],
      'helpId': self.help_id,
      'componentSetId': self.component_set_id,
      'versionId': self.component_set_version_id,
      'includeTagModifiers': self.tag_modifiers
    }

  @staticmethod
  def from_json(json):
    return DynamicComponent( \
      json.get('id'), \
      json.get('type'), \
      json.get('section'), \
      json.get('label'), \
      json.get('displayName'), \
      json.get('displayNameTemplate'), \
      json.get('icon'), \
      [Properties.Property.from_json(x) for x in json.get('properties', [])], \
      json.get('helpId'),
      json.get('componentSetId'), \
      json.get('versionId'),
      json.get('position', 'right')\
      json.get('includeTagModifiers', True)
    )

  def read(self, data):
    result_data = {}
    for prop in self.properties:
      result_data[prop.name] = prop.read(data)

    result_data = trigger_read_handlers(self.__class__, result_data)

    return result_data
