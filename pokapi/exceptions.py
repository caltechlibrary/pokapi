'''
exceptions.py: exceptions defined by Pokapi

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code is
open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''


# Base class.
# .............................................................................
# The base class makes it possible to use a single test to distinguish between
# exceptions generated by Pokapi and exceptions generated by something else.

class PokapiException(Exception):
    '''Base class for Pokapi exceptions.'''
    pass


# Exception classes.
# .............................................................................

class FolioError(PokapiException):
    '''Unrecoverable problem involving interactions with the Folio server.'''
    pass

class DataMismatchError(PokapiException):
    '''Unrecoverable problem involving Pokapi.'''
    pass

class NotFound(PokapiException):
    '''A requested item was not found in the Folio server.'''
    pass
