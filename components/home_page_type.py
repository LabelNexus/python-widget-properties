from .base_component import BaseComponent
import behavior
import pyro
import aws

class HomePageTypeComponent(BaseComponent):
  def __init__(self):
    super().__init__('home', 'page-type', 'General', 'Home', None, 'icon-url', self.get_properties())

  def get_properties(self):
    return [
      behavior.Properties.Property(None, 'Manifest', 'displayName', 'Name', 'text', default='Home'),
      behavior.Properties.Property(None, 'Manifest', 'shortName', 'Short Name', 'text', default='Home'),
      behavior.Properties.Property(None, 'Manifest', 'backgroundColor', 'Background Color', 'color', default='#fff'),
      behavior.Properties.Property(None, 'Manifest', 'themeColor', 'Theme Color', 'color', default='#fff'),
      behavior.Properties.Property(None, 'Manifest', 'icon', 'Icon', 'image-upload'),
      behavior.Properties.Property(None, 'Manifest', 'favicon', 'Fav Icon', 'image-upload')
    ]

  def read(self, data):
    # use to test if we uploaded a new version of the image
    # after the call to super the ephemeral key is removed so the check
    # needs to be done first
    icon_key = data.get('icon', {}).get('ephemeralKey', None)
    favicon_key = data.get('favicon', {}).get('ephemeralKey', None)

    val = super().read(data)

    # the base image property is already generating thumbnails for the image
    # so instead of trying to create manifest sizes from the original
    # ephemeral let's use the image we created the base image property.
    # this also prevents the issue of ending up with two different keys in
    # s3 in which the base image thumbnail key is saved with the record
    if icon_key is not None:
      pyro.Request.ExperienceCloud().post('/iot/v1/icons/manifest', {
        'key': val.get('icon', {}).get('key')
      })

    if favicon_key is not None:
      pyro.Request.ExperienceCloud().post('/iot/v1/icons/favicon', {
        'key': val.get('favicon', {}).get('key')
      })

    return val
