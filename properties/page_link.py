from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class PageLinkPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'page-link'

  def read(self, data):
    val = super().read(data)
    if val is None:
      val = {}

    result = {}

    result['mode'] = val.get('mode', 'page')
    if result['mode'] not in ['page', 'custom']:
      raise ValidationException('Invalid mode: ' + result['mode'])

    if result['mode'] == 'custom':
      result['url'] = val.get('url')
    else:
      result['instanceId'] = val.get('instanceId')
      if result['instanceId']:
        instance = Request.ExperienceCloud().get('/iot/v1/widget-instances/{}'.format(result['instanceId']))
        result['url'] = instance['url']
      else:
        result['url'] = ''

    return result
