drop procedure if exists sp_get_day_los_angeles;

DELIMITER //
CREATE PROCEDURE sp_get_day_los_angeles
  (IN days INT)
  BEGIN
    SET time_zone = 'America/Los_Angeles';
    call sp_get_day(days);
  END //
DELIMITER ;
