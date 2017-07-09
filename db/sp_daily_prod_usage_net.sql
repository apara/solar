drop procedure if exists sp_daily_prod_usage_net;

DELIMITER //
CREATE PROCEDURE sp_daily_prod_usage_net
  (IN DAYS_BACK INT)
  BEGIN
    -- Configure from and to
    --
    SET @TS_FROM = DATE_SUB(CURDATE(), INTERVAL DAYS_BACK day);
    SET @TS_TO = DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL DAYS_BACK day),"%Y-%m-%d 23:59:59");

    -- PROD, USAGE, NET
    --
    select
      @TS_FROM as 'from',
      @TS_TO as 'to',
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
  END //
DELIMITER ;
