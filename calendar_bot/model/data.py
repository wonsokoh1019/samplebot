#!/bin/env python
# -*- coding: utf-8 -*-
"""
sendMessage hello
"""

import json


# Action (ref:https://developers.worksmobile.com/kr/document/1005050?lang=ko)
# PostbackAction
def make_i18n_label(language, label):
    return {"language": language, "label": label}


def i18n_display_text(language, display_text):
    return {"language": language, "displayText": display_text}


def make_postback_action(data, display_text=None, label=None,
                         i18n_labels=None, i18n_display_texts=None):

    action = {"type": "postback", "data": data}

    if display_text is not None:
        action["displayText"] = display_text
    if label is not None:
        action["label"] = label
    if i18n_labels is not None:
        action["i18nLabels"] = i18n_labels
    if i18n_display_texts is not None:
        action["i18nDisplayTexts"] = i18n_display_texts

    return action


def i18n_text(language, text):
    return {"language": language, "text": text}


def make_message_action(label, post_back,
                        text=None, i18n_labels=None, i18n_texts=None):

    action = {"type": "message", "label": label, "postback": post_back}
    if text is not None:
        action["text"] = text
    if i18n_labels is not None:
        action["i18nLabels"] = i18n_labels
    if i18n_texts is not None:
        action["i18nTexts"] = i18n_texts

    return action


# URLAction
def make_url_action(label, url, i18n_labels=None):

    if i18n_labels is not None:
        return {"type": "uri", "label": label, "url": url,
                "i18nLabels": i18n_labels}
    return {"type": "uri", "label": label, "url": url}


# CameraAction, CameraRollAction, LocationAction
def make_normal_action(atype, label, i18n_labels=None):
    if i18n_labels is not None:
        return {"type": atype, "label": label, "i18nLabels": i18n_labels}
    return {"type": atype, "label": label}


# Quick reply :https://developers.worksmobile.com/kr/document/100500807?lang=ko
def make_i18n_thumbnail_image_url(language, thumbnail_image_url):
    return {"language": language, "thumbnailImageUrl": thumbnail_image_url}


def make_i18n_image_resource_id(language, image_resource_id):
    return {"language": language, "imageResourceId": image_resource_id}


def make_quick_reply_item(action,
                          url=None,
                          image_resource_id=None,
                          i18n_thumbnail_image_urls=None,
                          i18n_image_resource_ids=None):
    reply_item = {"action": action}
    if url is not None:
        reply_item["imageUrl"] = url
    if image_resource_id is not None:
        reply_item["imageResourceId"] = image_resource_id
    if i18n_thumbnail_image_urls is not None:
        reply_item["i18nImageUrl"] = i18n_thumbnail_image_urls
    if i18n_image_resource_ids is not None:
        reply_item["i18nImageResourceIds"] = i18n_image_resource_ids
    return reply_item


def make_quick_reply(replay_items):
    return {"items": replay_items}

# text (https://developers.worksmobile.com/kr/document/100500801?lang=ko)
# def make_i18n_text(language, text):
#    return {"language":language, "text":text}


def make_text(text, i18n_texts=None):
    if i18n_texts is not None:
        return {"type": "text", "text": text, "i18nTexts": i18n_texts}
    return {"type": "text", "text": text}


"""
Image Carousel:
(ref:https://developers.worksmobile.com/kr/document/100500809?lang=ko)
Request URL
https://apis.worksmobile.com/r/{API ID}/message/v1/bot/{botNo}/message/push
HTTP Method
POST (Content-Type: application / json; charset = UTF-8)
"""


def make_i18n_image_url(language, image_url):
    return {"language": language, "imageUrl": image_url}


def make_image_carousel_column(image_url=None,
                               image_resource_id=None,
                               action=None,
                               i18n_image_urls=None,
                               i18n_image_resource_ids=None):
    column_data = {}
    if image_url is not None:
        column_data["imageUrl"] = image_url
    if image_resource_id is not None:
        column_data["imageResourceId"] = image_resource_id
    if action is not None:
        column_data["action"] = action
    if i18n_image_urls is not None:
        # [MakeI18nImageUrl, MakeI18nImageUrl]
        column_data["i18nImageUrls"] = i18n_image_urls
    if i18n_image_resource_ids is not None:
        # [MakeI18nImageResourceId, MakeI18nImageResourceId, ...]
        column_data["i18nImageResourceIds"] = i18n_image_resource_ids
    return column_data


def make_image_carousel(columns):
    return {"type": "image_carousel", "columns": columns}


"""
Rich Menu:
Registering:
    https://wiki.navercorp.com/pages/viewpage.action?pageId=413524928
ref:
    https://developers.worksmobile.com/kr/document/1005040?lang=ko
    You can create a rich menu for the message bot by following these steps:
    Image uploads: using the "Upload Content" API
    Rich menu generation: using the "Register Message Rich Menu" API
    Rich Menu Image Settings: Use the "Message Rich Menu Image Settings" API
    ...
"""


def make_size(w, h):
    return {"width": w, "height": h}


def make_bound(x, y, w, h):
    return {"x": x, "y": y, "width": w, "height": h}


def make_area(bound, action):
    return {"bounds": bound, "action": action}


def make_add_rich_menu(name, size, areas):
    return {"name": name, "size": size, "areas": areas}


"""
button
"""


def make_i18n_content_texts(language, content_text):
    return {"language": language, "contentText": content_text}


def make_button(text, actions, content_texts=None):
    if content_texts is not None:
        return {"type": "button_template", "contentText": text,
                "i18nContentTexts": content_texts, "actions": actions}
    return {"type": "button_template", "contentText": text, "actions": actions}
