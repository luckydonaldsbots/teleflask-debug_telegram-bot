from pytgbot.api_types.sendable.reply_markup import ReplyKeyboardMarkup, KeyboardButton
from luckydonaldUtils.logger import logging
from teleflask import TBlueprint
from teleflask.messages import HTMLMessage

from html import escape
from .gitinfo import VERSION_STR
from .features import features

__author__ = 'luckydonald'
logger = logging.getLogger(__name__)

bot = TBlueprint(__name__)

class Lang():
    here_are_some_options = "Here are some options"
# end class

@bot.command('version')
def cmd_version(update, text):
    return HTMLMessage('Version <code>{version}</code> of bot <a href="tg://user?id={bot_id}">@{bot_username}</a>'.format(
        version=escape(VERSION_STR), bot_id=escape(str(bot.user_id)), bot_username=escape(bot.username)
    ))
# end def


@bot.command('do')
def cmd_do(update, text):
    options = [[KeyboardButton(txt) for txt in features.keys()]]
    return HTMLMessage(
        Lang.here_are_some_options,
        reply_markup=ReplyKeyboardMarkup(
            options,
            resize_keyboard=True,
            one_time_keyboard=True,
            selective=True
        ),
    )
# end def
