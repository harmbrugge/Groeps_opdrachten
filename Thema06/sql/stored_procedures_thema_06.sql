CREATE PROCEDURE sp_check_overlap(IN v_exp_id INT)

    BLOCK_ONE : BEGIN

    DECLARE v_finished BOOL DEFAULT 0;
    DECLARE v_gene_id INT;

    DECLARE c_gene_id_cursor
    CURSOR FOR SELECT
                 DISTINCT
                 genes_id_gene
               FROM db2_oligos;
    DECLARE CONTINUE HANDLER
    FOR NOT FOUND SET v_finished = 1;

    OPEN c_gene_id_cursor;

    get_duplicates: LOOP
      FETCH c_gene_id_cursor
      INTO v_gene_id;

      IF v_finished = 1
      THEN
        LEAVE get_duplicates;
      END IF;


        BLOCK_TWO: BEGIN

        DECLARE lp2_finished BOOL DEFAULT 0;
        DECLARE start_pos INT DEFAULT 0;
        DECLARE stop_pos INT DEFAULT 0;
        DECLARE oligo_id INT DEFAULT 0;
        DECLARE cur_start_pos INT;
        DECLARE cur_stop_pos INT;
        DECLARE cur_oligo_id INT;
        DECLARE cur_probe_id INT;
        DECLARE previous_oligo_state BOOL DEFAULT 0;

        DECLARE pos_check CURSOR FOR
          SELECT
            o.id_oligos,
            o.start_position,
            o.stop_position,
            p.id_probe
          FROM db2_oligos o JOIN db2_probes p ON p.oligos_id_oligos = o.id_oligos
          WHERE genes_id_gene = v_gene_id AND p.micro_arrays_id_micro_array = v_exp_id
          ORDER BY start_position ASC, stop_position ASC;

        DECLARE CONTINUE HANDLER
        FOR NOT FOUND SET lp2_finished = 1;

        OPEN pos_check;

        check_overlap: LOOP

          FETCH pos_check
          INTO cur_oligo_id, cur_start_pos, cur_stop_pos, cur_probe_id;

          IF lp2_finished = 1
          THEN
            LEAVE check_overlap;
          END IF;


          IF cur_start_pos < stop_pos OR cur_stop_pos > start_pos
          THEN

            CALL sp_mark_duplicate_oligos_man(TRUE, cur_probe_id);

          ELSE
            SELECT
              cur_oligo_id,
              cur_start_pos,
              cur_stop_pos
            INTO oligo_id, start_pos, stop_pos;
          END IF;

        END LOOP check_overlap;

      END BLOCK_TWO;
    END LOOP get_duplicates;

  END BLOCK_ONE $$