#!/usr/bin/env python3

import datetime


def list_of(type):
    """Return to_list such that to_list([x0, x1, ...]) returns
    [type(x0), type(x1), ...].
    """
    def to_list(x):
        return [type(e) for e in x]
    return to_list


def none_or(type):
    """Return to_type such that to_type(x) returns
    None if x is None else type(x).
    """
    def to_type(x):
        return None if x is None else type(x)
    return to_type


def to_datetime(x):
    """Convert a valid global date and time string
    (e.g. '2010-01-02T03:04:05Z') to the datetime.datetime object.
    """
    x = x.replace('Z', '+00:00').replace('T', ' ')
    x = x[:-3] + x[-2:]  # '...+XX:YY' -> '...+XXYY'
    try:
        return datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S%z')
    except ValueError:
        return datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f%z')


def _repr(self, *attrs):
    name = self.__class__.__name__
    body = ', '.join('{attr}={value!r}'.format(attr=a, value=getattr(self, a))
                     for a in attrs)
    return '<{name} {body}>'.format(name=name, body=body)


class Status(object):
    """Entry object"""
    __slots__ = (
        'link', 'created_at', 'favorited', 'haiku_text', 'html', 'html_touch',
        'html_mobile', 'id', 'in_reply_to_status_id', 'in_reply_to_user_id',
        'keyword', 'replies', 'source', 'target', 'text', 'user',
    )

    def __init__(self, d):
        super().__init__()
        self.link = str(d['link'])
        self.created_at = to_datetime(d['created_at'])
        self.favorited = int(d['favorited'])
        self.haiku_text = none_or(str)(d.get('haiku_text'))
        self.html = none_or(str)(d.get('html'))
        self.html_touch = none_or(str)(d.get('html_touch'))
        self.html_mobile = none_or(str)(d.get('html_mobile'))
        self.id = str(d['id'])
        raw = d.get('in_reply_to_status_id')
        self.in_reply_to_status_id = none_or(str)(raw)
        raw = d.get('in_reply_to_user_id')
        self.in_reply_to_user_id = none_or(str)(raw)
        self.keyword = none_or(str)(d.get('keyword'))
        self.replies = none_or(list_of(Status))(d.get('replies'))
        self.source = str(d['source'])
        self.target = none_or(Target)(d.get('target'))
        self.text = none_or(str)(d.get('text'))
        self.user = User(d['user'])

    def __repr__(self):
        return _repr(self, 'link')


class User(object):
    """User object"""
    __slots__ = (
        'followers_count', 'name', 'id', 'profile_image_url', 'screen_name',
        'url',
    )

    def __init__(self, d):
        super().__init__()
        self.followers_count = int(d['followers_count'])
        self.name = str(d['name'])
        self.id = str(d['id'])
        self.profile_image_url = str(d['profile_image_url'])
        self.screen_name = str(d['screen_name'])
        self.url = str(d['url'])

    def __repr__(self):
        return _repr(self, 'id')


class Keyword(object):
    """Keyword object"""
    __slots__ = (
        'entry_count', 'followers_count', 'link', 'related_keywords', 'title',
        'word', 'url_name',
    )

    def __init__(self, d):
        super().__init__()
        self.entry_count = int(d['entry_count'])
        self.followers_count = int(d['followers_count'])
        self.link = str(d['link'])
        raw = d.get('related_keywords')
        self.related_keywords = none_or(list_of(str))(raw)
        self.title = str(d['title'])
        self.word = str(d['word'])
        self.url_name = none_or(str)(d.get('url_name'))

    def __repr__(self):
        return _repr(self, 'word')


class Target(object):
    """Target object"""
    __slots__ = ('title', 'word', 'url_name',)

    def __init__(self, d):
        super().__init__()
        self.title = str(d['title'])
        self.word = str(d['word'])
        self.url_name = none_or(str)(d.get('url_name'))

    def __repr__(self):
        return _repr(self, 'word')
