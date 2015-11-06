Changelog
---------

* 2.5.0 Added asynchronous mode, added new endpoints for pylon.sample, and account.usage

* v.2.4.0 Added support for Open Data Processing (ODP) (2015-09-23)

* v.2.3.1 Removed twitter references, made it easier to provide alternative API URL (2015-09-02)

* v.2.1.1 Move to 1.2 of the API (2015-07-22)

* v.2.1.1 Added new historics_id parameter for DPU, fixed bug with POST requests (2015-05-21)

* v.2.1.0 Added support for PYLON (2015-05-15)

* v.2.0.13 Upgraded TLS security when streaming (2015-02-17)

  Big thanks to glyph from rackspace for helping us out with the Twisted SSL code

* v.2.0.11 Added support for pause and resume in historics (2014-08-27)

* v.2.0.10 Bumped to release stable version (2014-08-27)

* v.2.0.9 Bumped to release Dynamic Lists and new Managed Sources endpoints (2014-08-27)

* v.2.0.8 Bumped to release stable version (2014-06-04)

* v.2.0.7 Small bugfix for livestreaming (2014-05-09)

* v.2.0.6 Added windows support for livestreaming (2014-05-09)

* v.2.0.5 Added support for all 3 outputs in pull (2014-04-29)

* v.2.0.4 Upgraded the output mapper date logic to be more robust (2014-03-18)

* v.2.0.3 Fixed secure websockets on OpenSSL >1.0 (2014-02-20)

* v.2.0.2 Improved reconnection logic for livestreaming (2014-02-20)

* v.2.0.1 Fixed disconnect problems in livestreaming on slow streams (2014-02-19)

* v.2.0.0 Ground up rewrite. (2014-02-14)

* v.0.5.7 Fixed issues with buffers on reconnections (2013-06-28)

* v.0.5.6 Fixed broken tests, multistreaming, reconnection timeout (2013-05-03)

* v.0.5.5 Introduced automatic reconnection after 65 seconds of no data or ticks. Solves 'silent disconnect' issue (2013-03-06)

* v.0.5.4 Removed checks for existance of deprecated 'volume_info' field in historics/prepare response (2013-01-18)

* v.0.5.3 Added missing Historic sample size into historic/prepare requests (2012-12-03)

* v.0.5.2 Patch for the missing availability info after Historic/prepare [woozyking](https://github.com/woozyking) (2012-11-28)

* v.0.5.1 Removed unit tests that are no longer required (2012-08-30)

* v.0.5.0 Added support for Historic queries and Push delivery (2012-08-27)

* v.0.4.0 Fixed issues with SSL timeouts & low throughput streams (2012-08-08)

* v.0.3.0 Added SSL support and fixed a reconnection bug (2012-05-16)

  The SSL support is enabled by default and can be disabled by passing false as
  the third parameter to the User constructor, or calling enableSSL(false) on
  the User object.

* v.0.2.0 Fixed the handling of error messages in streams (2012-05-04)

* v.0.1.1 Initial release (2012-03-09)
