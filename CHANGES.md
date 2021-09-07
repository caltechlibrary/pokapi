# Change log for Pokapi

## Version 0.0.2

* Added more parameters to `Folio` interface object in order to avoid hardwiring Caltech-specific things into the code.
* Removed thumbnail handling code; it doesn't belong here because FOLIO/Okapi doesn't have a way to get thumbnails. What Pokapi was doing before was something more closely related to EDS.
* Changed fields in `FolioRecord` objects.
* Made numerous internal changes and bug fixes.


## Version 0.0.1

Started project and created PyPI placeholder.
