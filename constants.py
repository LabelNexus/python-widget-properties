EXPERIENCE_CLOUD_FACTORY = None

PROPERTY_COMPONENTS_READ_HANDLERS = {}

def add_read_handler(obj_type, handler):
  if obj_type not in PROPERTY_COMPONENTS_READ_HANDLERS:
    PROPERTY_COMPONENTS_READ_HANDLERS[obj_type] = []

  PROPERTY_COMPONENTS_READ_HANDLERS[obj_type].append(handler)

def trigger_read_handlers(obj_type, data):
  for x in PROPERTY_COMPONENTS_READ_HANDLERS.get(obj_type, []):
    data = x(data)

  return data
