# Change log for Pokapi

## Version 0.2.0

This release changes the parsing of authors to use the text that appears in the `title` field of the Folio record instead of the contributors list field.


## Version 0.1.0

This release includes breaking changes to the API:
* The parameter `page_template` is gone from the `Folio` object.
* The field `details_page` is gone from the `FolioRecord` object.

These changes were made after the realization that the record pages were not a concept of FOLIO or Okapi, but rather of the discovery system, and thus they don't belong in Pokapi.


## Version 0.0.2

* Added more parameters to `Folio` interface object in order to avoid hardwiring Caltech-specific things into the code.
* Removed thumbnail handling code; it doesn't belong here because FOLIO/Okapi doesn't have a way to get thumbnails. What Pokapi was doing before was something more closely related to EDS.
* Changed fields in `FolioRecord` objects.
* Made numerous internal changes and bug fixes.


## Version 0.0.1

Started project and created PyPI placeholder.
