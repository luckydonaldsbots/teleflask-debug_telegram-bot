# -*- coding: utf-8 -*-
import json
from html import escape

from luckydonaldUtils.logger import logging
from pytgbot.api_types import TgBotApiObject
from pytgbot.api_types.receivable.updates import Update, CallbackGame
from pytgbot.api_types.sendable.reply_markup import InlineKeyboardMarkup, InlineKeyboardButton
from teleflask import TBlueprint
from teleflask.messages import TextMessage, HTMLMessage

from .utils import msg_get_reply_params

__author__ = 'luckydonald'
logger = logging.getLogger(__name__)

""" Stores dict string -> function to call with buttons """
features = {}  # "Text": function

bot = TBlueprint(__name__)


@bot.on_message('text')
def msg_text_features(update, msg):
    if not msg or not msg.text:
        return
    # end def
    text = msg.text.strip()
    if text in features:
        feat_func = features[text]
        logger.debug('feature command {!r} calling function {}(update, text)'.format(text, feat_func.__name__))
        return feat_func(update, text)
    # end if
# end def


def add_feature(string):
    def add_feature_inner(function):
        features[string] = function
        return function
    # end def
    return add_feature_inner
# end def


def format_api_result(obj: TgBotApiObject):
    string = 'null'
    if isinstance(obj, TgBotApiObject):
        if obj._raw:
            string = json.dumps(obj._raw, indent=4, sort_keys=True, ensure_ascii=False)
        else:
            string = json.dumps(obj.to_array(), indent=4, sort_keys=True, ensure_ascii=False)
        # end if
    # end def
    return HTMLMessage(
        "Type <code>{type}</code>:\n<pre>{msg}</pre>".format(type=escape(obj.__class__.__name__), msg=escape(string)),
    )
# end def


@add_feature('Game Message')
def feat_game(update: Update, text):
    chat_id = update.message.chat.id
    game_msg = bot.bot.send_game(chat_id, "test00", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(text="test me", callback_game=CallbackGame())],
    ]))
    return format_api_result(game_msg)
# end def

