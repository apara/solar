drop procedure if exists sp_get_day;

DELIMITER //
CREATE PROCEDURE sp_get_day
  (IN days INT)
  BEGIN
    -- Maximum DC power for the day
    --
    SET @date_ref=(CURDATE() - INTERVAL days DAY);
    SET @from_date=DATE_FORMAT(@date_ref,'%Y-%m-%d 00:00:00');
    SET @to_date=DATE_FORMAT(@date_ref,'%Y-%m-%d 23:59:59');

    SELECT
      ts,
      serial,
      round(avg_dc_power_kw * 1000) as avg_dc_power_w
    FROM
      v_line
    WHERE
      ts BETWEEN @from_date and @to_date
    ORDER BY
      ts,
      serial;

  END //
DELIMITER ;
