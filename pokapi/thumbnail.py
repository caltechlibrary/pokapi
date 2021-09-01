'''
thumbnail.py: utilities for getting jacket cover thumbnail images

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

from   commonpy.network_utils import net
from   lxml import etree, html
import json

if __debug__:
    from sidetrack import log

from .exceptions import DataMismatchError


# Internal constants.
# .............................................................................

_GOOGLE_SEARCH_URL = 'https://www.googleapis.com/books/v1/volumes?q={}'
_OPEN_LIBRARY_SEARCH_URL = 'http://covers.openlibrary.org/b/{}/{}-{}.jpg'


# Exported functions.
# .............................................................................

def thumbnail_url_for_pub(value):
    if not value:
        return ''
    else:
        return thumbnail_url_from_ol(value) or thumbnail_url_from_google(value)


def thumbnail_url_from_google(value):
    '''Given an ISBN, return a URL for an cover image thumbnail.'''
    # We can't currently handle ISSN's.
    if probable_issn(value):
        return ''
    (response, error) = net('get', _GOOGLE_SEARCH_URL.format(value))
    if error:
        return ''
    # Google returns JSON, making it easier to get data directly.
    json_dict = json.loads(response.content.decode())
    if 'items' not in json_dict:
        return ''
    if 'volumeInfo' not in json_dict['items'][0]:
        return ''
    info = json_dict['items'][0]['volumeInfo']
    if 'imageLinks' in info and 'thumbnail' in info['imageLinks']:
        return info['imageLinks']['thumbnail']
    return ''


def thumbnail_url_from_ol(value):
    '''Given an ISBN, return a URL for an cover image thumbnail.'''
    # Open Library's service doesn't handle ISSN's.
    if probable_issn(value):
        return ''
    for size in ['L', 'M', 'S']:
        url = _OPEN_LIBRARY_SEARCH_URL.format('isbn', value, size)
        (response, error) = net('get', url)
        if not error and response.status_code == 200:
            # If OL doesn't find a value, it returns a 1x1 pixel image.
            return url if len(response.content) > 810 else None
    return ''


# Internal utilities.
# .............................................................................

def probable_issn(value):
    return len(value) < 10 and '-' in value
