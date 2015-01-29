SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS, UNIQUE_CHECKS = 0;
SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0;
SET @OLD_SQL_MODE = @@SQL_MODE, SQL_MODE = 'TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Table `th6_blasted_oligos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `th6_blasted_oligos` ;

CREATE TABLE IF NOT EXISTS `th6_blasted_oligos` (
  `oligo_id` INT NULL,
  `gene_id` VARCHAR(100) NULL,
  `identity` FLOAT NULL,
  `alignment_len` INT NULL,
  `nr_mismatched` INT NULL,
  `nr_gaps` INT NULL,
  `start_pos` INT NULL,
  `stop_pos` INT NULL,
  `sbjct_start_pos` INT NULL,
  `sbjct_stop_pos` INT NULL,
  `e_value` FLOAT NULL,
  `score` FLOAT NULL,
  `id` INT NOT NULL AUTO_INCREMENT,

  PRIMARY KEY (`id`),
  INDEX `fk_th6_blasted_oligos_th6_oligos1_idx` (`oligo_id` ASC),
  CONSTRAINT `fk_th6_blasted_oligos_th6_oligos1`
    FOREIGN KEY (`oligo_id`)
    REFERENCES `th6_oligos` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SET SQL_MODE = @OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS;