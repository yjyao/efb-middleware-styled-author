from ehforwarderbot import Middleware
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
