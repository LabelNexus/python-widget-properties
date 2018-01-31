from .base_component import BaseComponent
from ..constants import EXPERIENCE_CLOUD_FACTORY
from ..properties import Properties

class HomePageTypeComponent(BaseComponent):
  def __init__(self):
    super().__init__('home', 'page-type', 'General', 'Home', None, 'icon-url', self.get_properties())

  def get_properties(self):
    dn_help_text = """
    Provides a human-readable name for the application as it is intended to be
    displayed to the user, for example among a list of other applications or
    as a label for an icon.
    """

    sn_help_text = """
    Provides a short human-readable name for the application. This is intended
    for use where there is insufficient space to display the full name of the
    web application.
    """

    bc_help_text = """
    Defines the expected background color for the web application. This value
    repeats what is already available in the application stylesheet, but can
    be used by browsers to draw the background color of a web application when
    the manifest is available before the style sheet has loaded. This creates
    a smooth transition between launching the web application and loading the
    application's content.
    """

    tc_help_text = """
    Defines the default theme color for an application. This sometimes affects
    how the application is displayed by the OS (e.g., on Android's task
    switcher, the theme color surrounds the application).
    """

    ic_help_text = """
    Used to identify the application in variety of contexts, such as when
    an experience is sent via SMS.
    """

    fc_help_text = """
    Used to identify the application when a small image format is required,
    such as when a browser is rendering the favicon
    """

    return [
      Properties.Property(None, 'Manifest', 'displayName', 'Name', 'text', default='Home', help_text=dn_help_text),
      Properties.Property(None, 'Manifest', 'shortName', 'Short Name', 'text', default='Home', help_text=sn_help_text),
      Properties.Property(None, 'Manifest', 'backgroundColor', 'Background Color', 'color', default='#fff', help_text=bc_help_text),
      Properties.Property(None, 'Manifest', 'themeColor', 'Theme Color', 'color', default='#fff', help_text=tc_help_text),
      Properties.Property(None, 'Manifest', 'icon', 'Splash Screen Icon', 'image-upload', help_text=ic_help_text),
      Properties.Property(None, 'Manifest', 'favicon', 'Favicon', 'image-upload', help_text=fc_help_text)
    ]
