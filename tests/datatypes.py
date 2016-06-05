#!/usr/bin/env pthon3


STATUS = {
    'link': 'http://h.hatena.ne.jp/xxxx/XXXX',
    'created_at': '2010-01-02T03:04:05Z',
    'favorited': '12',
    'haiku_text': 'HaikuText',
    'html': 'HTML',
    'html_touch': 'HTMLTouch',
    'html_mobile': 'HTMLMobile',
    'id': 'XXXX',
    'in_reply_to_status_id': 'YYYY',
    'in_reply_to_user_id': 'yyyy',
    'keyword': 'Word',
    'replies': [
        {
            'link': 'http://h.hatena.ne.jp/zzzz/ZZZZ',
            'created_at': '2009-06-07T08:09:10Z',
            'favorited': '1',
            'haiku_text': 'HaikuText2',
            'html': 'HTML2',
            'html_touch': 'HTMLTouch2',
            'html_mobile': 'HTMLMobile2',
            'id': '299864227873641485',
            'source': 'web',
            'text': 'Text2',
            'user': {
                'followers_count': '409',
                'name': 'Name2',
                'id': 'zzzz',
                'profile_image_url': 'http://zzzz/',
                'screen_name': 'zzzz',
                'url': 'http://h.hatena.ne.jp/zzzz/'
            },
        },
    ],
    'source': 'API',
    'target': {'title': 'Title', 'word': 'Word', 'url_name': 'URLName'},
    'text': 'Text',
    'user': {
        'followers_count': '123',
        'name': 'Name',
        'id': 'xxxx',
        'profile_image_url': 'http://xxxx/',
        'screen_name': 'xxxx',
        'url': 'http://h.hatena.ne.jp/xxxx/'
    },
}


USER = {
    'followers_count': '123',
    'name': 'Name',
    'id': 'ID',
    'profile_image_url': 'http://xxxx/',
    'screen_name': 'ScreenName',
    'url': 'http://h.hatena.ne.jp/ID',
}


KEYWORD = {
    'entry_count': '123',
    'followers_count': '456',
    'link': 'http://h.hatena.ne.jp/Word',
    'related_keywords': ['word1', 'word2'],
    'title': 'Title',
    'word': 'Word',
    'url_name': 'URLName',
}


TARGET = {
    'title': 'Title',
    'word': 'Word',
    'url_name': 'URLName',
}
