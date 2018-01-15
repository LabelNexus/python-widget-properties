from flask import current_app

class ImageBase:
  def read_image(self, val):
    if val is None:
      val = {}
    data = {
      'ephemeralKey': val.get('ephemeralKey'),
      'key': val.get('key')
    }

    #if data['ephemeralKey']:
    #  return EXPERIENCE_CLOUD_FACTORY.post('/iot/v1/files/upload', data)

    no_image = 'ec-location' + '/iot/v1/icons/no_image_available.png'
    return {
      'key': val.get('key'),
      'version': val.get('version'),
      'preview': val.get('preview', no_image),
      'previewLarge': val.get('previewLarge', no_image),
      'previewMedium': val.get('previewMedium', no_image),
      'previewSmall': val.get('previewSmall', no_image)
    }
