SET time_zone = 'America/Los_Angeles';


SET @DAYS_BACK = 2;
SET @TS_FROM = DATE_SUB(CURDATE(), INTERVAL @DAYS_BACK day);
SET @TS_TO = DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL @DAYS_BACK day),"%Y-%m-%d 23:59:59");
select @DAYS_BACK, @TS_FROM, @TS_TO;


-- PROD, USAGE, NET
--
select
	p.production, 
	p.net, 
	p.production + p.net as 'usage'
from
	(
		select
			(
				select
					sum(l.total_lifetime_energy_delta_kwh)
				from
					line l
				where
					l.type=130 and
					l.ts between @TS_FROM AND @TS_TO
			) as 'production',
			(
				SELECT
					((select l.total_lifetime_energy_kwh from line l where l.type = 140 and l.ts between @TS_FROM AND @TS_TO order by l.ts desc limit 1) - 
					(select l.total_lifetime_energy_kwh from line l where l.type = 140 and l.ts between @TS_FROM AND @TS_TO order by l.ts asc limit 1) )
			) as 'net'	
	) AS p;


-- Today's net
--
SELECT
	((select l.total_lifetime_energy_kwh from line l where l.type = 140 and l.ts between @TS_FROM AND @TS_TO order by l.ts desc limit 1) - 
	(select l.total_lifetime_energy_kwh from line l where l.type = 140 and l.ts between @TS_FROM AND @TS_TO order by l.ts asc limit 1) );

-- Today's production
--
select
	sum(l.total_lifetime_energy_delta_kwh)
from
	line l
where
	l.type=130 and
	l.ts between @TS_FROM AND @TS_TO;


select
	(
		select
			sum(l.total_lifetime_energy_delta_kwh) as 'production'
		from
			line l
		where
			l.type=130 and
			l.ts between @TS_FROM AND @TS_TO
	) as 'production',
	(
		SELECT
			((select l.total_lifetime_energy_kwh from line l where l.type = 140 and l.ts between @TS_FROM AND @TS_TO order by l.ts desc limit 1) - 
			(select l.total_lifetime_energy_kwh from line l where l.type = 140 and l.ts between @TS_FROM AND @TS_TO order by l.ts asc limit 1) ) as 'net'
	) as 'net';		


	
-- PROD, USAGE, NET
--
select
	p.production, 
	p.net, 
	p.production + p.net as 'usage'
from
	(
		select
			(
				select
					sum(l.total_lifetime_energy_delta_kwh)
				from
					line l
				where
					l.type=130 and
					l.ts between @TS_FROM AND @TS_TO
			) as 'production',
			(
				SELECT
					((select l.total_lifetime_energy_kwh from line l where l.type = 140 and l.ts between @TS_FROM AND @TS_TO order by l.ts desc limit 1) - 
					(select l.total_lifetime_energy_kwh from line l where l.type = 140 and l.ts between @TS_FROM AND @TS_TO order by l.ts asc limit 1) )
			) as 'net'	
	) AS p;

	
-- SELECT @@global.time_zone, @@session.time_zone;


-- Create a new composite view
--
drop view if exists v_line;
if not exist create view v_line as
select 
	line.*,
	location.room,
	location.direction,
	location.index
from 
	line
inner join
	location on (line.serial = location.serial)
where 
	type=130
order by
	location.room,
	location.direction; 
	
-- Maximum DC power for the day
--
SET @interval=1;
SET @date_ref=(CURDATE() - INTERVAL @interval DAY);
SET @from_date=DATE_FORMAT(@date_ref,"%Y-%m-%d 00:00:00");
SET @to_date=DATE_FORMAT(@date_ref,"%Y-%m-%d 23:59:59");

select @date_ref, @to_date;

select
	SUBSTRING_INDEX(GROUP_CONCAT(ts ORDER BY ts), ',', 1 ) AS 'From',
	SUBSTRING_INDEX(GROUP_CONCAT(ts ORDER BY ts desc), ',', 1 ) AS 'To',
	l.serial as 'Serial',
	l.direction as 'Direction',
	l.room as 'Room', 
	l.index as 'Index',
	round(avg(l.avg_dc_power_kw * 1000)) as 'Watt DC',
	round(avg(l.avg_ac_power_kw * 1000)) as 'Watt AC',
	round(avg((l.avg_dc_power_kw - l.avg_ac_power_kw)*1000)) as 'DC-AC',
	round(avg(l.inverter_temp_f)) as 'Temp',
	round(avg(l.total_lifetime_energy_kwh)) as 'Total Lifetime kWh',
	round(avg(lm.period_energy_kwh * 1000)) as 'Period Energy Wh'
from 
	v_line l
inner join (
	select 
		serial, 
		sum(total_lifetime_energy_delta_kwh) as period_energy_kwh,
		max(avg_dc_power_kw) as avg_dc_power_kw
	from
		v_line
	where
		ts between @from_date and @to_date
	group by
		serial
	) as lm
on 
	l.serial = lm.serial and l.avg_dc_power_kw = lm.avg_dc_power_kw
where
	l.ts between @from_date and @to_date
group by 
	l.serial
order by
	l.direction,
	l.room,
	l.avg_dc_power_kw;	
	
-- Maximum lifetime production
--
select
	l.id, 
	l.ts,
	l.serial as 'Serial',
	l.direction as 'Direction',
	l.room as 'Room', 
	l.inverter_temp_f as 'Temp',
	l.total_lifetime_energy_kwh as 'Total Energy kWh'
from 
	v_line l
inner join (
	select 
		serial, 
		max(total_lifetime_energy_kwh) as total_lifetime_energy_kwh
	from
		line
	where
		ts between date(now()) and now()
	group by
		serial
	) as lm
on 
	l.serial = lm.serial and l.total_lifetime_energy_kwh = lm.total_lifetime_energy_kwh
where
		l.ts between date(now()) and now()
order by
	l.total_lifetime_energy_kwh;



	 
