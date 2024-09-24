--filtering for individual property sales, since lots of the data records multi-property acquisitions where total sale price is repeated for each individual property

WITH subquery AS (
SELECT sales_date, sales_amount, street_number, street_code, street_name, nom_commune 
  , CASE
      WHEN premise_type = "Maison" THEN 1 # making house or apartment value binary
      ELSE 0
    END AS is_house
  , surface, sales_price_m2, number_of_principal_rooms, latitude, longitude
  , CASE
      WHEN LENGTH(municipality_code) > 5 THEN LEFT(municipality_code,5)
      ELSE municipality_code
    END AS municipality_code # cleaning municipality code since some have '.0' on the end 
  , CONCAT(sales_date,"_",sales_amount,"_",municipality_code) AS sale_key # concatenating values to create unique sale key 
FROM personalprojects-427117.prello.notary_real_estate_sales
WHERE sales_amount > 50000 AND sales_amount < 32861251 AND sales_date IS NOT NULL AND municipality_code IS NOT NULL # ensuring no null values mess up the key
)
, subquery2 AS (
SELECT sale_key
  , COUNT(sale_key) AS counter
FROM subquery
GROUP BY sale_key # grouping by sale_key to count number of listed sale prices for each one
HAVING counter = 1 # filtering to just include individual property sales rather than large scale real estate purchases, and filtering out any potential duplicates or mistakes in the data
)
SELECT *
FROM subquery2
LEFT JOIN subquery # rejoining relevant info columns from original table onto filtered list from subquery2
USING (sale_key)


