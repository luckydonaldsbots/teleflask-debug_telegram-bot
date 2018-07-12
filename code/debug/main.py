# -*- coding: utf-8 -*-
import json

from pytgbot.api_types.receivable.updates import Update
from luckydonaldUtils.logger import logging
from flask import Flask, request, jsonify
from teleflask import Teleflask
from teleflask.messages import HTMLMessage
from html import escape
import requests

from .gitinfo import VERSION_STR
from .secrets import API_KEY, HOSTNAME, URL_PATH, EVENT_CHANNEL

__author__ = 'luckydonald'
logger = logging.getLogger(__name__)

VERSION = "0.0.1"
__version__ = VERSION

logging.add_colored_handler(level=logging.DEBUG)


app = Flask(__name__)

bot = Teleflask(API_KEY, app)


def to_json_remove_api_key(func):
    """
    Jsonfify returned stuff, if dict or list
    Then set mimetype to "text/json"

    :param func: the function to wrap
    :return:
    """
    from functools import wraps
    @wraps(func)
    def remove_api_key_inner(*args, **kwargs):
        response = func(*args, **kwargs)
        if isinstance(response, (dict, list)):
            import json
            response = json.dumps(response)
        # end if
        if isinstance(response, str):
            response_kwargs = {}
            response_kwargs.setdefault("mimetype", "text/json")
            from flask import Response
            return Response(response.replace(API_KEY, "<API_KEY>"), **response_kwargs)
        # end if
        return response
    # end def inner
    return remove_api_key_inner
# end def


@app.route("/info/<api_key>/<command>")
@to_json_remove_api_key
def info(api_key, command):

    """
    Issue commands. E.g. /info/getMe

    :param command:
    :return:
    """
    if api_key != API_KEY:
        error_msg = "Wrong API key: {wrong_key}".format(wrong_key=api_key)
        logger.warning(error_msg)
        return error_msg, 403
    # end if
    logger.debug("COMMAND: {cmd}, ARGS: {args}".format(cmd=command, args=request.args))
    return repr(bot.bot.do(command, **request.args)).replace(API_KEY, "<API_KEY>")
# end def


@bot.on_update()
def income(update):
    assert isinstance(update, Update)
    reply_chat_id, reply_message_id = msg_get_reply_params(update)
    if reply_chat_id is None:
        logger.error("could not find chat:\n{}".format(update))
        reply_chat_id = EVENT_CHANNEL
    # end if
    if update._raw:
        string = json.dumps(update._raw, indent=4, sort_keys=True, ensure_ascii=False)
    else:
        string = json.dumps(update.to_array(), indent=4, sort_keys=True, ensure_ascii=False)
    # end if
    return HTMLMessage(
        "<code>{}</code>".format(string),
        receiver=reply_chat_id, reply_id=reply_message_id
    )
# end def


def msg_get_reply_params(update):
    # reply_chat_id, reply_message_id = \
    reply_chat_id, reply_message_id = bot.msg_get_reply_params(update)
    if reply_chat_id is not None:
        return reply_chat_id, reply_message_id
    # end if
    return reply_chat_id, reply_message_id

    if update.message and update.message.chat.id and update.message.message_id:
        reply_chat_id, reply_message_id = update.message.chat.id, update.message.message_id
    # end if
    if update.channel_post and update.channel_post.chat.id and update.channel_post.message_id:
        reply_chat_id, reply_message_id = update.channel_post.chat.id, update.channel_post.message_id
    # end if
    if update.edited_message and update.edited_message.chat.id and update.edited_message.message_id:
        reply_chat_id, reply_message_id = update.edited_message.chat.id, update.edited_message.message_id
    # end if
    if update.edited_channel_post and update.edited_channel_post.chat.id and update.edited_channel_post.message_id:
        reply_chat_id, reply_message_id = update.edited_channel_post.chat.id, update.edited_channel_post.message_id
    # end if
    if update.callback_query and update.callback_query.message and update.callback_query.message.chat and update.callback_query.message.chat.id and update.callback_query.message.message_id:
        reply_message_id, reply_chat_id = update.callback_query.message.message_id, update.callback_query.message.chat.id
    # end if
# end def


@bot.command('version')
def cmd_version(update, text):
    return HTMLMessage('<code>{version}</code>'.format(version=escape(VERSION_STR)))
# end def


@app.route("/")
def hello():
    return "<h1>Your advertisements could be here!</h1>"
# end def

@app.route("/healthcheck")
@to_json_remove_api_key
def healthcheck():
    overall_status = True
    # TODO

    status = {
        "health": overall_status,
    }
    status_response = jsonify(status)
    """:type status_status_response: Response"""
    status_code = 200 if overall_status else 500
    return status_response, status_code
# end def



if __name__ == "__main__":  # no nginx
    # "__main__" means, this python file is called directly.
    # not to be confused with "main" (because main.py) when called from from nginx
    app.run(host='0.0.0.0', debug=True, port=80)  # python development server if no nginx
# end if

