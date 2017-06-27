drop procedure if exists sp_get_max_dc;

DELIMITER //
CREATE PROCEDURE sp_get_max_dc
  (IN i_interval INT)
  BEGIN
    -- Maximum DC power for the day
    --
    SET @interval=i_interval;
    SET @date_ref=(CURDATE() - INTERVAL @interval DAY);
    SET @from_date=DATE_FORMAT(@date_ref,'%Y-%m-%d 00:00:00');
    SET @to_date=DATE_FORMAT(@date_ref,'%Y-%m-%d 23:59:59');

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
        on l.serial = lm.serial and l.avg_dc_power_kw = lm.avg_dc_power_kw
    where
      l.ts between @from_date and @to_date
    group by
      l.serial
    order by
      l.avg_dc_power_kw;

  END //
DELIMITER ;
