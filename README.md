# Atlas of Oregon Lakes

[![Build Status](https://travis-ci.org/PSU-OIT-ARC/aol.svg?branch=master)](https://travis-ci.org/PSU-OIT-ARC/aol)

## Technology stack

- PostgreSQL 10
- PostGIS 2.4
- Python 3.7
- Django 2.2.x
- ArcGIS (Cloud/SaaS)

## Getting started

To build the application dependencies in your host's environment:

    make init

To prepare the database you may use, e.g., the `import_database` command to install a copy of production data.

To use the provided Docker container definitions:

    venv/bin/docker-compose up -d

To authenticate with the provided default user:

    username: foobar@example.com
    password: foobar

## Deploying

This project using the Emcee tooling to define and orchestrate resource provisioning and deployment.
See the AWS cloudformation templates in `cloudformation` and the command definitions in `commands.py`
for more information.

## General notes

It's very important to create an index like this:

    CREATE INDEX observation_gist
    ON observation
    USING GIST (ST_BUFFER(ST_TRANSFORM(the_geom, 3644), 10));

This allows you to do intersection queries like:

    ST_BUFFER(ST_TRANSFORM(the_geom, 3644), 10) && (SELECT the_geom FROM lake_geom WHERE reachcode = %s)

with *very* good performance. The magic '10' is arbitrary, but you should keep this consistent with
DISTANCE_FROM_ITEM in lakes.models.

We **cannot** do this in a migration unfortunately, since the observation table is part of a different application/schema

Some custom migrations exist that add fields (like an hstore), and setup stored procs and triggers. So don't go blindly deleting them.
