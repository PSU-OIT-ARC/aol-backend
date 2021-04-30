# Change Log for Atlas of Oregon Lakes

## 1.5.6 - 2021-04-27

- Uses X-Sendfile semantics to deliver lake assets.
- Adds 'Content-Disposition' header to document requests in
  order to use a more human-friendly attachment filename.
- Updates package dependency versions.

## 1.5.5 - 2021-03-31

- Uses Emcee 1.1.
- Updates package dependency versions.

## 1.5.4 - 2021-02-26

- Updates package dependency versions.
- Revises Emcee command module implementation to modernize
  database client configuration and add swapfile provisioning.

## 1.5.3 - 2020-11-20

- Uses Emcee 1.0.6.
- Removes support for Python 3.5.
- Updates package dependency versions.

## 1.5.2 - 2020-09-09

- Updates package dependency versions.

## 1.5.1 - 2020-06-09

- Updates package dependency versions.

## 1.5.0 - 2020-03-26

- Adds custom domain support for 'oregonlakesatlas.org'

## 1.5.0.rc2 - 2020-02-13

- Updates package dependency versions.
- Uses new releases of 'emcee', 'cloud-config'.

## 1.5.0.rc1 - 2019-10-21

This release series signficantly revises the structure, implementation
and composition of the AOL project such that its primary purpose is
to provide backend support to the new AOL frontend application.

- Uses the Django 2.2 LTS release.
- Supports the new AOL frontend application.

## 1.4.0 - 2019-05-06

- Configures the project to use the 'emcee.backends.aws' backend.
- Uses the Django 1.11 LTS release.
- Updates Python dependencies.

## 1.3.3 - 2019-03-07

- Updates ODFW fishing report URL.

## 1.3.2 - 2016-11-04

- Revert ldap3 requirement to older version to fix lookup error.

## 1.3.1 - 2016-11-03

- Fix ckeditor urls in production

## 1.3.0 - 2016-10-25

- Fix CAS account url patterns.
- Adds Sentry Support.

## 1.3b1 - 2016-03-28

Modernize:

- Make into a proper package: add setup.py w/ minimal requirements;
  separate dev from base/prod requirements; add MANIFEST.in.
- Replace Makefile with new & improved version.
- Replace wsgi.py with new version from ARCUtils.
- Fix Travis CI config.
- Use ARCTasks for init, releasing, deploying, etc.
- Upgrade ARCUtils from unreleased 1.x to released 2.x.
- Upgrade to Shibboleth CAS (via ARCUtils 2).
- Switch from varlet to django-local-settings.
- Don't import `django.conf.settings` as `SETTINGS`.
- Convert `urlpatterns` to plain list.
- Remove unused settings.
- Fix some migration names (include leading `000N_`).
- Jettison the local `User` model because it didn't serve any purpose
  and just made things confusing. NOTE: The `user` table will need to be
  renamed to `auth_user` and the `last_login` field will need to be
  altered to allow `NULL`s.
- Remove media directory with test JPEG; we can construct fake files in
  the tests instead.
- Use `{% static ... %}` instead of `{{ STATIC_URL }}...`.
- Add template blocks for CSS and JS.
- Move all JS to bottom of `<body>` where it belongs.
- Remove `type="text/javascript"` from `<script>` tags.

## 1.2.0 - 2015-09-02

### Added

- Travis stuff
- Upgraded django


## 1.1.0 - 2015-07-23

### Added

- Authentication is now based on LDAP group membership


## 1.0.1 - 2015-03-18

### Fixed

- The has_plants cached field is now updated when loadplantdata is called

### Added

- Documentation to the loadplantdata management command


## 1.0.0 - 2015-02-27

### Added

- Everything
