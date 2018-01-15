from .base_component import BaseComponent
from ..constants import EXPERIENCE_CLOUD_FACTORY
from ..properties import Properties
import aws

class HomePageTypeComponent(BaseComponent):
  def __init__(self):
    super().__init__('home', 'page-type', 'General', 'Home', None, 'icon-url', self.get_properties())

  def get_properties(self):
    return [
      Properties.Property(None, 'Manifest', 'displayName', 'Name', 'text', default='Home'),
      Properties.Property(None, 'Manifest', 'shortName', 'Short Name', 'text', default='Home'),
      Properties.Property(None, 'Manifest', 'backgroundColor', 'Background Color', 'color', default='#fff'),
      Properties.Property(None, 'Manifest', 'themeColor', 'Theme Color', 'color', default='#fff'),
      Properties.Property(None, 'Manifest', 'icon', 'Icon', 'image-upload'),
      Properties.Property(None, 'Manifest', 'favicon', 'Fav Icon', 'image-upload')
    ]
