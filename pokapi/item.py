'''
item.py: the FolioItem object class for Pokapi

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

from .record import FolioRecord


# Class definitions.
# .............................................................................

class FolioItem():
    '''Object class for representing an item within a record in FOLIO.'''

    # The reason for an explicit list of fields here is so that we can use it
    # in the definition of __repr__().
    __fields = {
        'item_id'       : str,          # id
        'hrid'          : str,          # hrid
        'holdings_id'   : str,          # holdingsRecordId
        'barcode'       : str,          # barcode
        'call_number'   : str,          # itemLevelCallNumber
        'material_type' : str,          # materialType.name
        'status'        : str,          # status.name
        'tags'          : str,          # tagsList, as a list
        'parent'        : type(FolioRecord),
    }

    def __init__(self, **kwargs):
        # Always first initialize every field.
        for field, field_type in self.__fields.items():
            setattr(self, field, ('' if field_type == str else None))
        # Set values if given arguments.
        for field, value in kwargs.items():
            setattr(self, field, value)


    def __str__(self):
        details = f' {self.barcode}' if self.barcode else ''
        return f'FolioItem{details}'


    def __repr__(self):
        field_values = []
        for field in sorted(self.__fields.keys()):
            value = getattr(self, field, None)
            printed_value = value if isinstance(value, list) else f'"{value}"'
            field_values.append(f'{field}={printed_value}')
        return 'FolioItem(' + ', '.join(field_values) + ')'


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
        return self.barcode < other.barcode


    def __gt__(self, other):
        if isinstance(other, type(self)):
            return other.barcode < self.barcode
        return NotImplemented


    def __le__(self, other):
        if isinstance(other, type(self)):
            return not other.barcode < self.barcode
        return NotImplemented


    def __ge__(self, other):
        if isinstance(other, type(self)):
            return not self.barcode < other.barcode
        return NotImplemented
