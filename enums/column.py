from enum import Enum

# Be sure to update properties/data_column_components.py with property mappings when adding to this enum
class ColumnDataType(str, Enum):
  BOOLEAN = 'boolean'
  DATETIME = 'datetime'
  DROPDOWN = 'dropdown'
  NUMERIC = 'numeric'
  TEXT = 'text'
  FILE = 'file'
  RICHTEXT = 'richtext'
  DOCUMENT = 'document'
  IMAGE = 'image'
  VIDEO = 'video'
