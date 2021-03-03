import os
class Settings():

  @staticmethod
  def get_setting(name, default_value=None):
    return os.environ.get(name, default_value)
