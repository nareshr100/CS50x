--CREATE INDEX movie_index2 ON directors(movie_id);
--CREATE INDEX person_index2 ON directors(person_id);

SELECT name FROM people
WHERE people.id IN (
SELECT DISTINCT directors.person_id
FROM directors JOIN ratings ON directors.movie_id = ratings.movie_id
WHERE rating >= 9.0)