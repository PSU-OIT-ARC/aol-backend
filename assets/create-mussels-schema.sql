DROP SCHEMA IF EXISTS mussels CASCADE;
CREATE SCHEMA mussels;

CREATE TABLE mussels.observation
(
    waterbody_id integer,
    specie_id smallint,
    date_checked date,
    physical_description text,
    agency_id integer,
    approved boolean,
    clr_substrate_id smallint,
    user_id integer,
    observation_id serial NOT NULL
);
CREATE TABLE mussels.specie (
    specie_id integer PRIMARY KEY,
    name text
);
CREATE TABLE mussels.agency (
    agency_id integer PRIMARY KEY,
    name text
);

SELECT AddGeometryColumn('mussels', 'observation', 'the_geom', 4326, 'POINT', 2);
