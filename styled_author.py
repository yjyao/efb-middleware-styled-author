from ehforwarderbot import Middleware
from ehforwarderbot import coordinator
from ehforwarderbot import utils as efb_utils
from functools import wraps
from ruamel.yaml import YAML
from telegram.parsemode import ParseMode
from telegram.replymarkup import ReplyMarkup
import html
import logging

from .__version__ import __version__ as version

class StyledAuthor(Middleware):
  '''Apply styles to message senders in group chats.'''

  middleware_id = 'styled_author.styled_author.StyledAuthor'
  middleware_name = 'StyledAuthor Middleware'
  __version__ = version

  logger = logging.getLogger(f'plugins.{middleware_id}')

  AUTHOR_START_TAG = f'{{{middleware_id}_START}}'
  AUTHOR_END_TAG = f'{{{middleware_id}_END}}'

  AUTHOR_STYLE_STARTS = {
    'italic': {
      ParseMode.HTML: '<i>',
      ParseMode.MARKDOWN: '__',
      ParseMode.MARKDOWN_V2: '_',
    },
    'bold': {
      ParseMode.HTML: '<b>',
      ParseMode.MARKDOWN: '**',
      ParseMode.MARKDOWN_V2: '*',
    },
  }

  AUTHOR_STYLE_ENDS = {
    'italic': {
      ParseMode.HTML: '</i>',
      ParseMode.MARKDOWN: '__',
      ParseMode.MARKDOWN_V2: '_',
    },
    'bold': {
      ParseMode.HTML: '</b>',
      ParseMode.MARKDOWN: '**',
      ParseMode.MARKDOWN_V2: '*',
    },
  }

  def __init__(self, instance_id=None):
    super().__init__(instance_id=instance_id)
    self.load_config()
    etm = coordinator.master
    (etm.slave_messages.
     generate_message_template) = self._override_generate_message_template(
       etm.slave_messages.generate_message_template)
    (etm.bot_manager.updater.bot._message) = self._override_tg_bot_message(
      etm.bot_manager.updater.bot._message)

  def load_config(self):
    try:
      config = YAML().load(efb_utils.get_config_path(self.middleware_id))
    except FileNotFoundError:
      config = {}
    self.AUTHOR_STYLE = config.get('author_style', 'italic')
    self.author_style_starts = self.AUTHOR_STYLE_STARTS[self.AUTHOR_STYLE]
    self.author_style_ends = self.AUTHOR_STYLE_ENDS[self.AUTHOR_STYLE]

  def _override_generate_message_template(self, old_generate_message_template):
    @wraps(old_generate_message_template)
    def wrapper(*args, **kwargs):
      msg_template = old_generate_message_template(*args, **kwargs)
      if msg_template:
        msg_template = '{}{}{}'.format(
          self.AUTHOR_START_TAG, msg_template, self.AUTHOR_END_TAG)
      return msg_template
    return wrapper

  def _override_tg_bot_message(self, old_tg_bot_message):
    @wraps(old_tg_bot_message)
    def wrapper(*args, **kwargs):
      data = (len(args) > 1 and args[1]) or kwargs.get('data', None)
      parsemode = data.get('parse_mode', None)
      data.setdefault('parse_mode', ParseMode.HTML)
      if data is not None:
        if data.get('caption'):
          data['caption'] = self._replace_author_tags(data['caption'], parsemode)
          self.logger.debug(f'Rewrote caption: {data["caption"]}')
        if data.get('text'):
          data['text'] = self._replace_author_tags(data['text'], parsemode)
          self.logger.debug(f'Rewrote text: {data["text"]}')
      if isinstance(kwargs.get('reply_markup', None), ReplyMarkup):
        for row in kwargs['reply_markup'].inline_keyboard:
          for button in row:
            # Inline buttons do not support styling yet.
            button.text = self._remove_author_tags(button.text)
            self.logger.debug(f'Rewrote keyboard button: {button.text}')
      return old_tg_bot_message(*args, **kwargs)
    return wrapper

  def _replace_author_tags(self, text, parsemode=None):
    if self.AUTHOR_START_TAG in text:
      if parsemode is None:
        text = html.escape(text)
        parsemode = ParseMode.HTML
      text = (text
              .replace(self.AUTHOR_START_TAG,
                       self.author_style_starts[parsemode])
              .replace(self.AUTHOR_END_TAG, self.author_style_ends[parsemode]))
    return text

  def _remove_author_tags(self, text):
    return (text #
            .replace(self.AUTHOR_START_TAG, '') #
            .replace(self.AUTHOR_END_TAG, ''))
