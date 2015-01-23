DROP PROCEDURE IF EXISTS mark_probes;

DELIMITER //

CREATE PROCEDURE mark_probes(IN v_exp_id INT)
  BEGIN
    DECLARE finished INTEGER DEFAULT 0;
    DECLARE v_oligo_id INT;
    DECLARE v_min INT;
    DECLARE v_max INT;
    DECLARE v_probe_length INT;


    SELECT
      min(id),
      max(id)
    FROM th6_oligos
    WHERE experiment_id = v_exp_id
    INTO v_min, v_max;

    SELECT set_probe_len
    FROM th6_experiment_settings
    WHERE id = v_exp_id
    INTO v_probe_length;

      BLOCK_ONE: BEGIN


      DECLARE c_blasted_oligos CURSOR FOR SELECT oligo_id
                                          FROM th6_blasted_oligos
                                          WHERE alignment_len = v_probe_length AND oligo_id BETWEEN v_min AND v_max
                                          GROUP BY oligo_id
                                          HAVING count(*) = 1;


      DECLARE CONTINUE HANDLER
      FOR NOT FOUND SET finished = 1;

      OPEN c_blasted_oligos;

      get_probes: LOOP
        IF finished = 1
        THEN
          LEAVE get_probes;
        END IF;

        FETCH c_blasted_oligos
        INTO v_oligo_id;

        UPDATE th6_oligos
        SET blast = TRUE
        WHERE id = v_oligo_id;

      END LOOP get_probes;

    END BLOCK_ONE;

  END //

DELIMITER ;