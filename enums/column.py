from enum import Enum

class ColumnDataType(str, Enum):
  BOOLEAN = 'boolean'
  DATETIME = 'datetime'
  DROPDOWN = 'dropdown'
  MULTISELECT = 'multiselect'
  NUMERIC = 'numeric'
  CURRENCY = 'currency'
  TEXT = 'text'
  FILE = 'file'
  RICHTEXT = 'richtext'
  DOCUMENT = 'document'
  IMAGE = 'image'
  VIDEO = 'video'
  ASSETDATA = 'asset-data'
  COUNTRY = 'country'