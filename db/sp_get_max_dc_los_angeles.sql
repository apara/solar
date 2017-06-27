drop procedure if exists sp_get_max_dc_los_angeles;

DELIMITER //
CREATE PROCEDURE sp_get_max_dc_los_angeles
  (IN i_interval INT)
  BEGIN
    SET time_zone = 'America/Los_Angeles';
    call sp_get_max_dc(i_interval);
  END //
DELIMITER ;
