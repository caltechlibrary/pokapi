'''
record.py: the FolioRecord object class for Pokapi

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

if __debug__:
    from sidetrack import log

from .exceptions import DataMismatchError


# Class definitions.
# .............................................................................

class FolioRecord():
    '''Object class for representing a record returned by FOLIO/Okapi.

    This object is at the level of abstraction corresponding to FOLIO's
    "instance" records. The "id" is the instance id.
    '''

    # The reason for an explicit list of fields here is so that we can use it
    # in the definition of __repr__().
    __fields = {
        'id'            : str,          # id of Folio instance record
        'details_page'  : str,          # URL to page in EDS
        'title'         : str,          # indexTitle
        'author'        : str,          # string concatenated from contributors
        'publisher'     : str,          # publication.publisher
        'year'          : str,          # publication.year
        'thumbnail_url' : str,          #
    }


    def __init__(self, server_url = None, **kwargs):
        # Internal variables.  Need to set these first.
        self._server_url = server_url
        self._saved_thumbnail_url = None

        # Always first initialize every field.
        for field, field_type in self.__fields.items():
            setattr(self, field, ([] if field_type == list else ''))
        # Set values if given arguments.
        for field, value in kwargs.items():
            setattr(self, field, value)


    def __getattribute__(self, attr):
        if attr == 'thumbnail_url':
            if self._saved_thumbnail_url is not None:
                return self._saved_thumbnail_url
            if __debug__: log(f'getting thumbnail url')
            self._saved_thumbnail_url = self._thumbnail_for_record()
            return self._saved_thumbnail_url
        return object.__getattribute__(self, attr)


    def __setattr__(self, attr, value):
        if attr == 'folio_id' and getattr(self, "_server_url", None):
            object.__setattr__(self, 'folio_url', f'{self._server_url}/record/{value}')
        object.__setattr__(self, attr, value)


    def __str__(self):
        details = f' {self.folio_id}' if self.folio_id else ''
        return f'FolioRecord{details}'


    def __repr__(self):
        field_values = []
        for field in sorted(self.__fields.keys()):
            value = getattr(self, field, None)
            printed_value = value if isinstance(value, list) else f'"{value}"'
            field_values.append(f'{field}={printed_value}')
        return 'FolioRecord(' + ', '.join(field_values) + ')'


    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return NotImplemented


    def __ne__(self, other):
        # Based on lengthy Stack Overflow answer by user "Maggyero" posted on
        # 2018-06-02 at https://stackoverflow.com/a/50661674/743730
        eq = self.__eq__(other)
        if eq is not NotImplemented:
            return not eq
        return NotImplemented


    def __lt__(self, other):
        return self.folio_id < other.folio_id


    def __gt__(self, other):
        if isinstance(other, type(self)):
            return other.folio_id < self.folio_id
        return NotImplemented


    def __le__(self, other):
        if isinstance(other, type(self)):
            return not other.folio_id < self.folio_id
        return NotImplemented


    def __ge__(self, other):
        if isinstance(other, type(self)):
            return not self.folio_id < other.folio_id
        return NotImplemented