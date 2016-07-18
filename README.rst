hatena-haiker: Hatena Haiku for Python 3
========================================

.. image:: https://img.shields.io/pypi/v/hatena-haiker.svg
    :target: https://pypi.python.org/pypi/hatena-haiker


hatena-haiker is an unofficial library
for the `Hatena Haiku <http://h.hatena.ne.jp/>`_ API.


Examples
--------

.. code-block:: python

    import haiker
    api = haiker.Haiker()
    for status in api.public_timeline(count=3, body_formats=['haiku']):
        created_at = status.created_at.strftime('%Y-%m-%d %H:%M:%S')
        print(created_at, status.user.id, status.keyword)
        print(status.haiku_text)
        print()

.. code-block:: python

    import haiker
    auth = haiker.OAuth('MyConsumerKey', 'MyConsumerSecret',
                        'MyAccessToken', 'MyAccessTokenSecret')
    api = haiker.Haiker(auth)
    status = api.update_status('BOT', 'Hello, world!', source='API')
    api.add_star(status.id)


Installation
------------

.. code-block:: bash

    pip3 install --upgrade hatena-haiker


Documentation
-------------

After completing the installation, execute the following:

.. code-block:: bash

    python3 -m pydoc haiker

