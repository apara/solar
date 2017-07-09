drop procedure if exists sp_daily_prod_usage_net_los_angeles;

DELIMITER //
CREATE PROCEDURE sp_daily_prod_usage_net_los_angeles
  (IN days INT)
  BEGIN
    SET time_zone = 'America/Los_Angeles';
    call sp_daily_prod_usage_net(days);
  END //
DELIMITER ;
