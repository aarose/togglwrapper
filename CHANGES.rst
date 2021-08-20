.. :changelog:

===============
Release History
===============

-------------------
2.0.0 - 2021.08.19
------------------
- Bumped major version since base API URL for Toggl changed `[#27] <https://github.com/aarose/togglwrapper/pull/27>`

- Switched to using __version__ to set version, instead of setting directly in setup.py

- (docs) Revamped docs with new version of Sphinx `[#33] <https://github.com/aarose/togglwrapper/pull/33>`

- (docs) Updated docs README for increased maintainability

- (chore) Bumped up dependency versions from dependabot suggestions (all dev-side updates).


-------------------
1.2.1 - 2021.03.25
------------------
- Don't pin ``requests`` in setup.py `[#10] <https://github.com/aarose/togglwrapper/pull/10>`_

- Bumped Sphinx docs dependencies to keep up-to-date (not used in core library)

- (ci) Added Dependabot config `[#12] <https://github.com/aarose/togglwrapper/pull/12>`_

-----
1.2.0
-----

Bug fix: Fixes issue #4 "Starting a time entry is POST not PUT".

Chores: Added notes on how to run tests, and how to generate docs.


-----
1.0.0
-----

Initial release. Supports Toggl's main API. Reports API not supported yet.
