SELECT name FROM people -- name of the id of stars with Kevin Bacon
WHERE name IS NOT 'Kevin Bacon' AND id IN (
SELECT person_id FROM stars -- get id of stars with Kevin Bacon
WHERE movie_id IN (
SELECT movie_id FROM stars -- get movie ids of all KB movies
WHERE person_id IN (
SELECT id FROM people -- get id of KB
WHERE name = 'Kevin Bacon' AND birth = 1958)));