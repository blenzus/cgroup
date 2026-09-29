-- 5. Total people born in each country

SELECT
    places.country,
    COUNT(*) AS total_births
FROM people
JOIN places
    ON people.place_of_birth = places.city
GROUP BY places.country
ORDER BY places.country;


-- 6. Cities and total births in each city

SELECT
    place_of_birth AS city,
    COUNT(*) AS total_births
FROM people
GROUP BY place_of_birth
ORDER BY place_of_birth;


-- 7. People born after January 1st 2000

SELECT
    id,
    given_name,
    family_name,
    date_of_birth,
    place_of_birth
FROM people
WHERE date_of_birth > '2000-01-01'
ORDER BY date_of_birth;