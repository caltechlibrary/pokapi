'''
folio.py: Interface to FOLIO

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

from   commonpy.interrupt import wait
from   commonpy.network_utils import net
from   commonpy.exceptions import NoContent, ServiceFailure, RateLimitExceeded
import json
from   json import JSONDecodeError

if __debug__:
    from sidetrack import log

from .exceptions import *
from .record import FolioRecord


# Constants.
# .............................................................................

# URL templates for retrieving data from a FOLIO/Okapi server.
_INSTANCE_FOR_BARCODE = '{}/inventory/instances?query=item.barcode%3D%3D{}'
_INSTANCE_FOR_INSTANCE_ID = '{}/instance-storage/instances/{}'

_ITEM_FOR_BARCODE = '{}/inventory/items?query=barcode%3D%3D{}'
_ITEM_FOR_ITEM_ID = '{}/inventory/items/{}'
_HOLDINGS_FOR_HOLDINGS_ID = '{}/holdings-storage/holdings/{}'


# Class definitions.
# .............................................................................

class Folio():
    '''Interface to a FOLIO server using Okapi.'''

    def __init__(self, okapi_url, okapi_token, tenant_id):
        '''Create an interface to the Folio server at "okapi_url".'''
        self.okapi_url = okapi_url
        self.okapi_token = okapi_token
        self.tenant_id = tenant_id


    def record(self, barcode = None, accession_number = None, instance_id = None):
        '''Create a FolioRecord object given a barcode, accession number, or
        instance id.  The arguments are mutually exclusive.

        This contacts the FOLIO server and perform a search using the id value,
        then using the data returned, create a FolioRecord object with an
        FolioRecord object within it, and finally return the FolioRecord
        object.  If the FOLIO server does not return a result, this method
        raises a NotFound exception.

        If no argument is given, this returns an empty FolioRecord.

        '''
        args = [barcode, accession_number, instance_id]
        if sum(map(bool, args)) > 1:
            raise ValueError(f'Keyword args to record() are mutually exclusive.')
        if barcode:
            return self._record_from_server(_INSTANCE_FOR_BARCODE, barcode)
        elif accession_number:
            # Accession numbers are based on instance id's.
            instance_id = id_from_an(accession_number)
            return self._record_from_server(_INSTANCE_FOR_INSTANCE_ID, instance_id)
        elif instance_id:
            return self._record_from_server(_INSTANCE_FOR_INSTANCE_ID, instance_id)
        else:
            return FolioRecord()


    def _record_from_server(self, url_fmt, identifier):
        def response_handler(resp):
            if not resp or not resp.text:
                if __debug__: log(f'got no response for {request_url}')
                return None
            data_dict = json.loads(resp.text)
            # Depending on the way we're getting it, the item record might be
            # directly provided or it might be in a list of records.
            if not 'totalRecords' in data_dict:
                if 'title' in data_dict:
                    # It's an item record.
                    return data_dict
                else:
                    raise FolioError('Unexpected data returned by FOLIO')
            elif data_dict['totalRecords'] == 0:
                if __debug__: log(f'got empty response for {request_url}')
                return None
            elif data_dict['totalRecords'] > 1:
                if __debug__: log(f'got multiple responses for {request_url}')
                if __debug__: log(f'using only first value')
            return data_dict['instances'][0]

        request_url = url_fmt.format(self.okapi_url, identifier)
        json_dict = self._result_from_api(request_url, response_handler)
        edition = json_dict['editions'][0] if len(json_dict['editions']) > 0 else ''
        return FolioRecord(instance_id   = json_dict['id'],
                           url           = '',
                           title         = json_dict['indexTitle'],
                           author        = pub_author(json_dict['contributors']),
                           year          = pub_year(json_dict['publication']),
                           edition       = edition,
                           thumbnail_url = '')


    def _result_from_api(self, url, result_producer, retry = 0):
        '''Do HTTP GET on "url" & return results of calling result_producer on it.'''
        headers = {
            "x-okapi-token": self.okapi_token,
            "x-okapi-tenant": self.tenant_id,
            "content-type": "application/json",
        }

        (resp, error) = net('get', url, headers = headers)
        if not error:
            if __debug__: log(f'got result from {url}')
            return result_producer(resp)
        elif isinstance(error, NoContent):
            if __debug__: log(f'got empty content from {url}')
            return result_producer(None)
        elif isinstance(error, RateLimitExceeded):
            retry += 1
            if retry > _MAX_SLEEP_CYCLES:
                raise FolioError(f'Rate limit exceeded for {url}')
            else:
                # Wait and then call ourselves recursively.
                if __debug__: log(f'hit rate limit; pausing {_RATE_LIMIT_SLEEP}s')
                wait(_RATE_LIMIT_SLEEP)
                return self._result_from_api(url, result_producer, retry = retry)
        else:
            raise FolioError(f'Problem contacting {url}: {str(error)}')


# Miscellaneous helpers.
# .............................................................................

def cleaned(text):
    '''Mildly clean up the given text string.'''
    if not text:
        return text
    text = text.rstrip('./')
    return text.strip()


def pub_year(publication_list):
    year = publication_list[0]['dateOfPublication']
    return ''.join(filter(str.isdigit, year))


def pub_author(contributors_list):
    return ' and '.join(author['name'] for author in contributors_list)


def parsed_title_and_author(text):
    '''Extract a title and authors (if present) from the given text string.'''
    title = None
    author = None
    # The possible formats we've seen so far:
    #   "title / author"
    #   "title / author; other info"
    if ';' in text:
        end = text.rfind(';')
        text = text[:end].strip()
    if text.find('/') > 0:
        start = text.find('/')
        title = text[:start].strip()
        author = text[start + 2:].strip()
    elif text.find('[by]') > 0:
        start = text.find('[by]')
        title = text[:start].strip()
        author = text[start + 5:].strip()
    elif text.rfind(', by') > 0:
        start = text.rfind(', by')
        title = text[:start].strip()
        author = text[start + 5:].strip()
    else:
        title = text
    if title.endswith(':'):
        title = title[:-1].strip()
    return title, author


def id_from_an(accession_number):
    start = accession_number.find('.')
    id_part = accession_number[start + 1:]
    return id_part.replace('.', '-')
