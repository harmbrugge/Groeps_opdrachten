SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

-- -----------------------------------------------------
-- Table `th6_chromosome`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `th6_chromosome` ;

CREATE  TABLE IF NOT EXISTS `th6_chromosome` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `external_id` VARCHAR(45) NULL ,
  `organism` VARCHAR(45) NULL ,
  `chromosome_def` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `th6_gene`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `th6_gene` ;

CREATE  TABLE IF NOT EXISTS `th6_gene` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `chromosome_id` INT NOT NULL ,
  `external_id` VARCHAR(45) NULL ,
  `sequence` TEXT NULL ,
  `start` INT NULL ,
  `stop` INT NULL ,
  `strand` CHAR(1) NULL ,
  `protein` VARCHAR(100) NULL ,
  `protein_id` VARCHAR(45) NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_gene_chromosome` (`chromosome_id` ASC) ,
  CONSTRAINT `fk_gene_chromosome`
    FOREIGN KEY (`chromosome_id` )
    REFERENCES `th6_chromosome` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `th6_probe_experiment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `th6_probe_experiment` ;

CREATE  TABLE IF NOT EXISTS `th6_probe_experiment` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `date` DATETIME NULL ,
  `set_mono_repeat` INT NULL ,
  `set_di_repeat` INT NULL ,
  `set_coverage` INT NULL ,
  `set_probe_len` INT NULL ,
  `count_mono_repeat` INT NULL ,
  `count_di_repeat` INT NULL ,
  `count_hairpin` INT NULL ,
  `time_total` FLOAT NULL ,
  `time_mono` FLOAT NULL ,
  `time_di` FLOAT NULL ,
  `time_hairpin` FLOAT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `th6_oligo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `th6_oligo` ;

CREATE  TABLE IF NOT EXISTS `th6_oligo` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `gene_id` INT NOT NULL ,
  `probe_experiment_id` INT NOT NULL ,
  `sequence` CHAR(25) NOT NULL ,
  `cg_perc` DOUBLE NULL ,
  `temp_melt` DOUBLE NULL ,
  `fraction` DOUBLE NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_oligo_gene1` (`gene_id` ASC) ,
  INDEX `fk_oligo_probe_experiment1` (`probe_experiment_id` ASC) ,
  CONSTRAINT `fk_oligo_gene1`
    FOREIGN KEY (`gene_id` )
    REFERENCES `th6_gene` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_oligo_probe_experiment1`
    FOREIGN KEY (`probe_experiment_id` )
    REFERENCES `th6_probe_experiment` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `th6_microarray`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `th6_microarray` ;

CREATE  TABLE IF NOT EXISTS `th6_microarray` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `hybrid_temp` DOUBLE NULL ,
  `min_temp` DOUBLE NULL ,
  `max_temp` DOUBLE NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `th6_probe`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `th6_probe` ;

CREATE  TABLE IF NOT EXISTS `th6_probe` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `microarray_id` INT NOT NULL ,
  `oligo_id` INT NOT NULL ,
  `pos_y` INT NULL ,
  `pos_x` INT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_probe_microarray1` (`microarray_id` ASC) ,
  INDEX `fk_probe_oligo1` (`oligo_id` ASC) ,
  CONSTRAINT `fk_probe_microarray1`
    FOREIGN KEY (`microarray_id` )
    REFERENCES `th6_microarray` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_probe_oligo1`
    FOREIGN KEY (`oligo_id` )
    REFERENCES `th6_oligo` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
