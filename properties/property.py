from .text import TextPropertyType
from .color import ColorPropertyType
from .image import ImagePropertyType
from .component import ComponentPropertyType
from .components import ComponentsPropertyType
from .checkbox import CheckboxPropertyType
from .toggle import TogglePropertyType
from .translated_text import TranslatedTextProperty
from .dropdown import DropdownPropertyType
from .dropdown_options import DropdownOptionsPropertyType
from .multiselect import MultiselectPropertyType
from .multiselect_chip import MultiselectChipPropertyType
from .tag_selector import TagSelectorPropertyType
from .numeric import NumericPropertyType
from .page_link import PageLinkPropertyType
from .page_slug_editor import PageSlugEditorPropertyType
from .code_editor import CodeEditorPropertyType
from .html_editor import HtmlEditorPropertyType
from .html_editor_view import HtmlEditorViewPropertyType
from .asset_data_select import AssetDataSelectPropertyType
from .theme_color import ThemeColorPropertyType
from .admin_launcher import AdminLauncherPropertyType
from .dynamic_component import DynamicComponentPropertyType
from .dynamic_components import DynamicComponentsPropertyType
from .dynamic_asset_select import DynamicAssetSelectPropertyType
from .data_column_components import DataColumnComponentsPropertyType
from .data_column_row_input import DataColumnRowInputPropertyType
from .font import FontPropertyType
from .asset_select import AssetSelectPropertyType
from .asset_container_select import AssetContainerSelectPropertyType
from .asset_field import AssetFieldPropertyType
from .asset_field_filter import AssetFieldFilterPropertyType
from .file_upload import FileUploadPropertyType
from .email_list import EmailListPropertyType
from .font_style import FontStylePropertyType
from .font_style_selector import FontStyleSelectorPropertyType
from .dynamic_property_list import DynamicPropertyListPropertyType
from .simple_html_editor import SimpleHtmlEditorPropertyType
from .simple_html_editor_view import SimpleHtmlEditorViewPropertyType
from .connection_field import ConnnectionFieldPropertyType
from lumavate_exceptions import ValidationException
from .data_source import DataSourcePropertyType
from .datetime import DateTimePropertyType
from .time_range import TimeRangePropertyType
from .video import VideoPropertyType
from .currency import CurrencyPropertyType
from .timezone import TimezonePropertyType
from .country import CountryPropertyType
from .content_asset_filter_select import ContentAssetFilterSelectPropertyType

class Property:
  def __init__(self, classification, section, name, label, property_type_name, options={}, default=None, help_text=None, additional_options={}):
    self.property_type = self.get_property_type(property_type_name)
    self.classification = classification
    self.section = section
    self.name = name
    self.label = label
    self.default = default
    self.property_type.property = self
    self.options = options
    self.help_text = help_text
    self.additional_options = additional_options

  @staticmethod
  def from_json(json):
    if json is None:
      return None

    return Property( \
      json.get('classification'), \
      json.get('section'), \
      json.get('name'), \
      json.get('label'), \
      json.get('type'), \
      options=json.get('options'), \
      default=json.get('default'), \
      help_text=json.get('helpText'),
      additional_options=json.get('additionalOptions'))

  def get_property_type(self, type_name):
    types = {
      'asset-select': AssetSelectPropertyType,
      'asset-container-select': AssetContainerSelectPropertyType,
      'asset-field': AssetFieldPropertyType,
      'asset-field-filter': AssetFieldFilterPropertyType,
      'data-source': DataSourcePropertyType,
      'text' : TextPropertyType,
      'color': ColorPropertyType,
      'image-upload': ImagePropertyType,
      'component': ComponentPropertyType,
      'components': ComponentsPropertyType,
      'checkbox': CheckboxPropertyType,
      'toggle': TogglePropertyType,
      'translated-text': TranslatedTextProperty,
      'dropdown': DropdownPropertyType,
      'dropdown-options': DropdownOptionsPropertyType,
      'multiselect': MultiselectPropertyType,
      'multiselect-chip': MultiselectChipPropertyType,
      'tag-selector': TagSelectorPropertyType,
      'numeric': NumericPropertyType,
      'page-link': PageLinkPropertyType,
      'page-slug-editor': PageSlugEditorPropertyType,
      'code-editor': CodeEditorPropertyType,
      'theme-color': ThemeColorPropertyType,
      'admin-launcher': AdminLauncherPropertyType,
      'html-editor': HtmlEditorPropertyType,
      'html-editor-view': HtmlEditorViewPropertyType,
      'simple-html-editor': SimpleHtmlEditorPropertyType,
      'simple-html-editor-view': SimpleHtmlEditorViewPropertyType,
      'dynamic-component': DynamicComponentPropertyType,
      'dynamic-components': DynamicComponentsPropertyType,
      'dynamic-asset-select': DynamicAssetSelectPropertyType,
      'asset-data-select': AssetDataSelectPropertyType,
      'data-column-components': DataColumnComponentsPropertyType,
      'data-column-row-input': DataColumnRowInputPropertyType,
      'font': FontPropertyType,
      'file-upload': FileUploadPropertyType,
      'email-list': EmailListPropertyType,
      'font-style': FontStylePropertyType,
      'font-style-selector': FontStyleSelectorPropertyType,
      'dynamic-property-list': DynamicPropertyListPropertyType,
      'connection-field': ConnnectionFieldPropertyType,
      'datetime': DateTimePropertyType,
      'time-range': TimeRangePropertyType,
      'video': VideoPropertyType,
      'currency': CurrencyPropertyType,
      'timezone': TimezonePropertyType,
      'country': CountryPropertyType,
      'content-asset-filter-select': ContentAssetFilterSelectPropertyType
    }

    prop_type = types.get(type_name)

    if prop_type is None:
      raise ValidationException('Unknown type name:' + type_name)

    return prop_type(self)

  def to_json(self):
    return {
      'classification': self.classification,
      'section': self.section,
      'name': self.name,
      'label': self.label,
      'type': self.property_type.type_name,
      'options': self.options,
      'default': self.default,
      'helpText': self.help_text,
      'additionalOptions': self.additional_options
    }

  def read(self, data):
    return self.property_type.read(data)
