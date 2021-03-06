SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

-- -----------------------------------------------------
-- Table `th6_organism`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `th6_organism` ;

CREATE  TABLE IF NOT EXISTS `th6_organism` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(60) NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `th6_chromosome`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `th6_chromosome` ;

CREATE  TABLE IF NOT EXISTS `th6_chromosome` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `organism_id` INT NOT NULL ,
  `external_id` VARCHAR(45) NULL DEFAULT NULL ,
  `organism` VARCHAR(45) NULL DEFAULT NULL ,
  `chromosome_def` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_chromosome_organism` (`organism_id` ASC) ,
  CONSTRAINT `fk_chromosome_organism`
    FOREIGN KEY (`organism_id` )
    REFERENCES `th6_organism` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `th6_gene`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `th6_gene` ;

CREATE  TABLE IF NOT EXISTS `th6_gene` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `chromosome_id` INT NOT NULL ,
  `external_id` VARCHAR(45) NULL DEFAULT NULL ,
  `sequence` TEXT NULL DEFAULT NULL ,
  `start` INT NULL DEFAULT NULL ,
  `stop` INT NULL DEFAULT NULL ,
  `strand` CHAR(1) NULL DEFAULT NULL ,
  `protein` VARCHAR(100) NULL DEFAULT NULL ,
  `protein_id` VARCHAR(45) NULL DEFAULT NULL ,
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
  `date` DATETIME NULL DEFAULT NULL ,
  `set_mono_repeat` INT NULL DEFAULT NULL ,
  `set_di_repeat` INT NULL DEFAULT NULL ,
  `set_coverage` INT NULL DEFAULT NULL ,
  `set_probe_len` INT NULL DEFAULT NULL ,
  `count_mono_repeat` INT NULL DEFAULT NULL ,
  `count_di_repeat` INT NULL DEFAULT NULL ,
  `count_hairpin` INT NULL DEFAULT NULL ,
  `count_gc` INT NULL DEFAULT NULL ,
  `count_possible` INT NULL DEFAULT NULL ,
  `count_total` INT NULL DEFAULT NULL ,
  `time_total` FLOAT NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `th6_oligo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `th6_oligo` ;

CREATE TABLE IF NOT EXISTS `th6_oligo` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `gene_id` INT NOT NULL,
  `probe_experiment_id` INT NOT NULL,
  `sequence` VARCHAR(25) NOT NULL,
  `cg_perc` DOUBLE NULL DEFAULT NULL,
  `temp_melt` DOUBLE NULL DEFAULT NULL,
  `fraction` DOUBLE NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_oligo_gene1` (`gene_id` ASC),
  INDEX `fk_oligo_probe_experiment1` (`probe_experiment_id` ASC),
  CONSTRAINT `fk_oligo_gene1`
    FOREIGN KEY (`gene_id`)
    REFERENCES `th6_gene` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_oligo_probe_experiment1`
    FOREIGN KEY (`probe_experiment_id`)
    REFERENCES `th6_probe_experiment` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `th6_microarray`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `th6_microarray` ;

CREATE  TABLE IF NOT EXISTS `th6_microarray` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `hybrid_temp` DOUBLE NULL DEFAULT NULL ,
  `min_temp` DOUBLE NULL DEFAULT NULL ,
  `max_temp` DOUBLE NULL DEFAULT NULL ,
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
  `pos_y` INT NULL DEFAULT NULL ,
  `pos_x` INT NULL DEFAULT NULL ,
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


-- -----------------------------------------------------
-- Table `th6_experiment_genes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `th6_experiment_genes` ;

CREATE  TABLE IF NOT EXISTS `th6_experiment_genes` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `th6_gene_id` INT NOT NULL ,
  `th6_probe_experiment_id` INT NOT NULL ,
  `count_mono_repeat` INT NULL DEFAULT NULL ,
  `count_di_repeat` INT NULL DEFAULT NULL ,
  `count_hairpin` INT NULL DEFAULT NULL ,
  `count_possible` INT NULL DEFAULT NULL ,
  `count_gc` INT NULL DEFAULT NULL ,
  `count_total` INT NULL DEFAULT NULL ,
  `time_total` FLOAT NULL ,
  `time_mono` FLOAT NULL ,
  `time_di` FLOAT NULL ,
  `time_gc` FLOAT NULL ,
  `time_hairpin` FLOAT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_experiment_genes_th6_gene1_idx` (`th6_gene_id` ASC) ,
  INDEX `fk_experiment_genes_th6_probe_experiment1_idx` (`th6_probe_experiment_id` ASC) ,
  CONSTRAINT `fk_experiment_genes_th6_gene1`
    FOREIGN KEY (`th6_gene_id` )
    REFERENCES `th6_gene` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_experiment_genes_th6_probe_experiment1`
    FOREIGN KEY (`th6_probe_experiment_id` )
    REFERENCES `th6_probe_experiment` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `table1`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `table1` ;

CREATE  TABLE IF NOT EXISTS `table1` (
  `id` INT NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
