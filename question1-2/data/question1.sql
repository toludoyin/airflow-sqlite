
select 
date_trunc('month', pickup_datetime) as month_date, 
avg(case when day_of_week=6 then trip_count else null end) as sat_avg_trips,      -- The average number of trips on Saturdays
round(avg(case when day_of_week=6 then fare_amount else null end),2) as sat_avg_fare,      --The average fare (fare_amount) per trip on Saturdays
round(avg(case when day_of_week=6 then trip_duration else null end),2) as sat_avg_durations,  --The average duration per trip on Saturdays
avg(case when day_of_week=0 then trip_count else null end) as sun_avg_trips,      --The average number of trips on Sundays
round(avg(case when day_of_week=0 then fare_amount else null end),2) as sun_avg_fare,       --The average fare (fare_amount) per trip on Sundays
round(avg(case when day_of_week=0 then trip_duration  else null end),2) as sun_avg_duration       --The average duration per trip on Sundays
from (
	select 
	pickup_date, 
	id, 
	fare_amount, 
	pickup_datetime, 
	dropoff_datetime, 
	toDayOfWeek(pickup_datetime) as day_of_week,
	count(id) over (partition by date_trunc('month', pickup_datetime), toDayOfWeek(pickup_datetime)) AS trip_count,
	dateDiff('minutes', pickup_datetime, dropoff_datetime) as trip_duration 
	from tripdata
	where pickup_date between '2014-01-01' and '2016-12-31'
) as trips_summary
group by month_date