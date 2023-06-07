import copy
from lumavate_properties import Properties, Components

class PatchRequest:
  def __init__(
      self,
      namespace,
      instance_id,
      prop,
      operation,
      value,
      parent_type,
      parent_name,
      is_component,
      component_id,
      component_type,
      component = None,
      old_component = None,
      root_name = None,
      parent_component_id = None
      ):
    self.namespace = namespace
    self.instanceId = instance_id
    self.property = prop
    self.operation = operation
    self.property_value = value
    self.parent_type = parent_type
    self.parent_name = parent_name
    self.is_component = is_component
    self.component_id = component_id
    self.component_type = component_type
    self.component = component
    self.old_component_set = old_component
    self.root_name = root_name
    self.is_child_component = root_name is not None
    self.parent_component_id = parent_component_id

  @staticmethod
  def from_json(json):
    if json is None:
      return None

    props = []
    component = None
    if json.get('operation') in ['add','replace','edit', 'copy', 'addChild', 'editChild']:
      component = copy.copy(json.get('componentDef', {}))
      if component is not None:
        component_props = component.get('properties',[])
        if component_props is not None:
          for p in component_props:
            props.append(Properties.Property.from_json(p))

        component['properties'] = props

    return PatchRequest(
        json.get('namespace'), \
        json.get('instanceId'), \
        Properties.Property.from_json(json.get('propertyDef')) if json.get('operation') is not 'delete' else None, \
        json.get('operation'), \
        json.get('propertyValue'), \
        json.get('parentType'), \
        json.get('parentName'), \
        json.get('isComponent'), \
        json.get('componentId'), \
        json.get('componentType'), \
        component, \
        json.get('oldComponentSet'),
        json.get('rootName'),
        json.get('parentComponentId')
        )

