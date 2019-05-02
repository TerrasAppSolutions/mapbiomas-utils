INSERT INTO territorios (id, descricao, categoria, the_geom)
SELECT featureid, name, categoria, geom
FROM paises_temp