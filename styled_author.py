from ehforwarderbot import Middleware
from ehforwarderbot import coordinator
from functools import wraps
import logging

from .__version__ import __version__ as version

class StyledAuthor(Middleware):
  '''Apply styles to message senders in group chats.'''

  middleware_id = 'styled_author.styled_author.StyledAuthor'
  middleware_name = 'StyledAuthor Middleware'
  __version__ = version

  logger = logging.getLogger(f'plugins.{middleware_id}')

  def __init__(self, instance_id=None):
    super().__init__(instance_id=instance_id)
    etm = coordinator.master
    (etm.slave_messages.
     generate_message_template) = self._override_generate_message_template(
       etm.slave_messages.generate_message_template)

  def _override_generate_message_template(self, old_generate_message_template):
    @wraps(old_generate_message_template)
    def wrapper(*args, **kwargs):
      msg_template = old_generate_message_template(*args, **kwargs)
      if msg_template:
        msg_template = f'<i>{msg_template}</i>'
      return msg_template
    return wrapper
