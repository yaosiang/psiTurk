# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.1]
### Added
- test suite to pave the way for migrating to Python 3 (woo!)
- Support for Python 3.6 and 3.7
- travis CI runs setup.py tests for python 2.7, 3.6, and 3.7
- table that tracks psiturk-created HITids in local db

### Changed
- `psiturk_shell` file does all printing through cmd2's `.poutput` so that stuff can be redirected
- `amt_services_wrapper` and `amt_services` functions are wrapped via decorator so that they return a consistent Response-type object. This
  effectively separates the `print`ing of any psiturk_shell data from the core psiturk functions. This will make a web interface doable. Also,
  it allows for the core functions to throw meaningful exceptions, which are caught by the wrapper and returned.
- psiturk status message is pulled from github repo instead of from an api call to the psiturk.org api server.
  Also, the call to load this does not depend directly on urllib2 anymore.
- update many dependencies because why not
 
### Removed
- Shell support for EC2 MySQL

### Fixed
- #352 - expiring a hit didn't push far enough into the past to actually expire instead of extend on the mturk side
