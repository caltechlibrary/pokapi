# Info about tests for Pokapi

The tests in this directory are meant to be run using [pytest](https://pytest.org). However, before you can run the tests, you need to set 3 variables:

* `OKAPI_URL`
* `OKAPI_TOKEN`
* `TENANT_ID`

These can be set as environment variables in the process running pytest, or they can be stored in a file called `settings.ini` placed in this directory. The file [`test_folio.py`](test_folio.py) expects to find the values of the variables when it runs, and will fail if it cannot find them.
