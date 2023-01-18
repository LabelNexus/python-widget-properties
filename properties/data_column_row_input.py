from jinja2 import Environment, BaseLoader
from flask import g
from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException
from lumavate_properties import enums

class DataColumnRowInputPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'data-column-row-input'

  @staticmethod
  def from_data_columns(columns):
    from .property import Property
    properties = []

    for column in columns:
      column_def = column.get('componentData',{})

      property_type = DataColumnRowInputPropertyType.get_column_property_mapping(column_def)
      options = DataColumnRowInputPropertyType.get_property_options(column_def)
      default = DataColumnRowInputPropertyType.get_property_default(property_type, options)
      properties.append(Property( 
        classification=None,
        section=None,
        name=column_def.get('columnName',''),
        label=column_def.get('columnDisplayName'),
        property_type_name=property_type,
        options=options,
        default=default,
        help_text='').to_json())

    return Property(
      classification=None,
      section=None,
      name='columns',
      label='column',
      property_type_name='data-column-row-input',
      options= {'properties': properties},
      default={},
      help_text='')


  @staticmethod
  def get_column_property_mapping(column_def):
    column_type = column_def.get('columnType',{}).get('value')

    return DataColumnRowInputPropertyType.column_property_mappings()[column_type]

  @staticmethod
  def get_property_options(column_def):
    column_type = column_def.get('columnType',{}).get('value')
    if column_type==enums.ColumnDataType.DOCUMENT:
      return DataColumnRowInputPropertyType.parse_document_options(column_def)

    if column_type==enums.ColumnDataType.DROPDOWN:
      return DataColumnRowInputPropertyType.parse_dropdown_options(column_def)
      
    if column_type==enums.ColumnDataType.IMAGE:
      return DataColumnRowInputPropertyType.parse_image_options(column_def)

    if column_type==enums.ColumnDataType.RICHTEXT:
      return DataColumnRowInputPropertyType.parse_richtext_options(column_def)

    options = column_def.get('columnType',{}).get('options',{})
    if options == '':
      options = {}
    return options

  @staticmethod
  def parse_dropdown_options(column_def):
    column_options = column_def.get('columnType',{}).get('options','')
    if not column_options:
      return {}

    options ={}
    for option in column_options.split(','):
      split_option = option.split('|')
      if len(split_option)==2:
        options[split_option[0].strip()] = split_option[1].strip()
      else:
        options[split_option[0].strip()] = split_option[0].strip()

    return options
  
  @staticmethod
  def parse_image_options(column_def):
    return {
      'hideDefaultSource': True
    }

  @staticmethod
  def parse_document_options(column_def):
    return {
      'allowPageSelect': False,
      'initialSource': 'asset'
    }

  @staticmethod
  def parse_richtext_options(column_def):
    return {
      'useStandardView': True,
      'initialSource': 'default'
    }

  @staticmethod
  def column_property_mappings():
    return {
      enums.ColumnDataType.BOOLEAN.value:  'toggle',
      enums.ColumnDataType.DATETIME.value: 'datetime',
      enums.ColumnDataType.DROPDOWN.value: 'dropdown',
      enums.ColumnDataType.NUMERIC.value: 'numeric',
      enums.ColumnDataType.TEXT.value: 'text',
      enums.ColumnDataType.FILE.value: 'file-upload',
      enums.ColumnDataType.RICHTEXT.value: 'simple-html-editor',
      enums.ColumnDataType.DOCUMENT.value: 'page-link',
      enums.ColumnDataType.IMAGE.value: 'image-upload',
      enums.ColumnDataType.VIDEO.value: 'video'
    }

  @staticmethod
  def get_property_default(property_type, property_options):
    if property_type == 'datetime':
      # TODO we dont hav a datetime type
      return ''
    elif property_type == 'dropdown':
      options = list(property_options.keys())
      if len(options)>0:
        return options[0]

      return ''
    elif property_type == 'file-upload':
      return property_options.get('default', {})
    elif property_type == 'image-upload':
      return property_options.get('default', {})
    elif property_type == 'numeric':
      return property_options.get('default', 0)
    elif property_type == 'page-link':
      return property_options.get('default', {})
    if property_type == 'toggle':
      return property_options.get('default',False)
    elif property_type == 'text':
      return property_options.get('default', '')
    elif property_type == 'simple-html-editor':
      return property_options.get('default', '')
    elif property_type == 'video':
      return property_options.get('default', {})

    return property_options.get('default', None)

  def read(self, data):
    return super().read(data)