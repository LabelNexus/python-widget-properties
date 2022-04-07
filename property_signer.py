
# workaround for sharing between services and platform
try:
  import pyro
except:
  from ._settings import Settings as pyro

from lumavate_signer import ValueHasher

class PropertySigner:
  def __init__(self):
    self._value_hasher = ValueHasher(pyro.get_setting('VALUE_HASHER_KEY'))

  def sign_properties(self, properties):
    component_types = ['component', 'components', 'dynamic-component', 'dynamic-components']
    for p in properties:
      if p['type'] in component_types:
        components = p.get('options',{}).get('components',[])
        for c in components:
          for cp in c.get('properties',[]):
            self._sign_property(cp)

        tag_modifiers = p.get('options',{}).get('tagModifiers',[])
        for t in tag_modifiers:
          self._sign_property(t)

      else:
        self._sign_property(p)

  def _sign_property(self, prop):
    prop_hash = self._value_hasher.sign(self.filter_signature_properties(prop))
    prop['signature'] = prop_hash

  # removes properties that are not part of the property definition
  # but are added during client or from server for performance reasons.
  # these properties should be excluded from the signature
  @classmethod
  def filter_signature_properties(cls,prop):
    excluded_keys = ['signature', 'hasComponentHelp', prop["name"], 'isNew']
    return {k: v for k,v in prop.items() if k not in excluded_keys}

