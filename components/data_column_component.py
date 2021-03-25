from flask import request, current_app
from ..constants import trigger_read_handlers
from ..properties import Properties
from .base_component import BaseComponent
import os

class DataColumnComponent(BaseComponent):
  def __init__(self, component_type, category, section, label, display_name, icon_url, properties, help_id=None, display_name_template=None, position='right'):
    super().init(
        component_type,
        category,
        section,
        label,
        display_name,
        icon_url,
        properties,
        help_id,
        display_name_template,
        position)

  @staticmethod
  def from_json(json):
    return DataColumnComponent( \
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

