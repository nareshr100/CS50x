SELECT title FROM
ratings JOIN movies ON ratings.movie_id = movies.id JOIN
stars ON stars.movie_id = movies.id JOIN
people ON stars.person_id = people.id
WHERE name = 'Chadwick Boseman'
ORDER BY rating DESC
LIMIT 5;