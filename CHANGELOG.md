# Change Log for Atlas of Oregon Lakes

## 1.3.0 - 2016-10-25

In progress...


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
