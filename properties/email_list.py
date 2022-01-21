from .text import TextPropertyType
from lumavate_exceptions import ValidationException
import re


class EmailListPropertyType(TextPropertyType):
  @property
  def type_name(self):
    return 'email-list'

  def read(self, data):
    val = super().read(data)

    emails = val.split(',')
    for email in emails: 
      if not re.fullmatch('[^@]+@[^@]+\.[^@]+', email.strip()):
        raise ValidationException(f'Email {email} is invalid ', api_field=self.property.name)

    return val


