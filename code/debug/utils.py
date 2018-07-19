# -*- coding: utf-8 -*-
from luckydonaldUtils.logger import logging
from teleflask.server.base import TeleflaskBase

from .secrets import API_KEY

__author__ = 'luckydonald'
logger = logging.getLogger(__name__)


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


def msg_get_reply_params(update):
    reply_chat_id, reply_message_id = TeleflaskBase.msg_get_reply_params(update)
    if reply_chat_id is not None:
        return reply_chat_id, reply_message_id
    # end if

    if update.inline_query and update.inline_query.from_peer and update.inline_query.from_peer.id:
        return update.inline_query.from_peer.id, None
    # end if

    return None, None
# end def
