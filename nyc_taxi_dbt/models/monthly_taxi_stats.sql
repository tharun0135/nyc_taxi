{{ config(materialized='table') }}

SELECT 
    date_trunc('month', tpep_pickup_datetime) as trip_month,
    count(*) as total_trips,
    round(avg(trip_distance), 2) as avg_distance_miles,
    round(avg(trip_duration_minutes), 2) as avg_duration_mins
FROM trips_cleaned
GROUP BY 1
ORDER BY 1
