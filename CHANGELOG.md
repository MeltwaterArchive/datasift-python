CHANGELOG
================================
## v.2.10.0 (2016-11-02)
### Added
* `service` param to PYLON API calls
* Support for new `/pylon/task` API
### Changed
* Now uses API v1.4 by default

## v2.9.0 (2016-08-03)
### Added
Added analyze limits to the identity.limit create and update, under analyze_queries argument

## v.2.8.1 (2016-03-02)
### Changed
Correctly released features intended for 2.8.0

## v.2.8.0 (2016-03-02)
### Changed
* Pylon endpoints now take and return a recording ID, rather than a hash
* Moved to v1.3 API

### Added
* Pylon/Update added for hotswapping filters

## v.2.7.0 (2016-02-18)
### Changed
* made full response available on the rate limited exception (exception.response)

### Added
* added the ability to disable date parsing with date_strings=True sent into the client object

## v.2.6.0 (2015-11-25)
### Changed
* Upgraded the version of pyopenssl we're using
* Clarified that Twisted support is broken on Windows with python3

## v.2.5.0 (2015-10-23)
### Added
* asynchronous mode, this is documented [here](http://datasift.github.io/datasift-python/async.html)
* added new endpoints for pylon.sample, and account.usage, these are also documented

## v.2.4.0 (2015-08-23)
### Added
* Support for [Open Data Processing](https://datasift.com/products/open-data-processing-for-twitter/) batch uploads

## v.2.3.1 (2015-09-02)
### Added
* api_host and api_version parameters are now available when creating a Client object
### Removed
* Twitter references from the examples, since it's no longer a supported source

## v.2.1.1 (2015-07-22)
### Added      <!-- New feature added -->
* historics_id has been added to the dpu function for measuring the dpu usage of a historics job
### Changed    <!-- Existing feature has been changed -->
* swapped to use the API's 1.2 version internally

## v. (v.2.1.0)
### Added
* PYLON module added under client.pylon, documentation available [here](http://datasift.github.io/datasift-python/datasift.html#datasift-pylon-module)
