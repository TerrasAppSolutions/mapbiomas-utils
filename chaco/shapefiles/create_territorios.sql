CREATE TABLE public.territorios (
    id integer NOT NULL PRIMARY KEY,
    descricao character varying(100),
    categoria character varying(100),
    the_geom geometry

);

ALTER TABLE territorios ADD CONSTRAINT territorios_id_key UNIQUE (id);

ALTER TABLE public.territorios OWNER TO terras;
