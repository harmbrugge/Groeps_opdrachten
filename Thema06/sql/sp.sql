DROP PROCEDURE IF EXISTS mark_probes;

DELIMITER //

CREATE PROCEDURE mark_probes()
  BEGIN
    DECLARE finished INTEGER DEFAULT 0;
    DECLARE oligo_id INT;

    DECLARE probes CURSOR FOR SELECT oligo_id
                              FROM th6_blasts
                              WHERE alignment_len = 20
                              GROUP BY oligo_id
                              HAVING count(*) = 1;

    DECLARE CONTINUE HANDLER
    FOR NOT FOUND SET finished = 1;

    OPEN probes;

    get_probes: LOOP
      FETCH probes
      INTO oligo_id;

      IF finished = 1
      THEN
        LEAVE get_probes;
      END IF;

      SELECT oligo_id;
      UPDATE th6_oligos SET blast = TRUE WHERE id = oligo_id;

    END LOOP get_probes;

  END //

DELIMITER ;