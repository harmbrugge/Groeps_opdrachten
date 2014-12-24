-- MySQL Script generated by MySQL Workbench
-- 12/24/14 10:33:21
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';


-- -----------------------------------------------------
-- Table `th6_computers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `th6_computers` ;

CREATE TABLE IF NOT EXISTS `th6_computers` (
  `id` INT NOT NULL,
  `pc_name` VARCHAR(100) NULL,
  `proccessor_id` VARCHAR(100) NULL,
  `clockspeed` INT NULL COMMENT 'In Mhz',
  `core_count` INT NULL,
  `ram_size` INT NULL COMMENT 'In Mb',
  `ram_speed` INT NULL COMMENT 'in Hz',
  `architecture` VARCHAR(100) NULL,
  `python_version` VARCHAR(100) NULL,
  `operating_sytem` VARCHAR(100) NULL,
  `kernel_version` VARCHAR(100) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `th6_benchmarks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `th6_benchmarks` ;

CREATE TABLE IF NOT EXISTS `th6_benchmarks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `comments` TEXT NULL,
  `mono_rep` INT NULL,
  `di_rep` INT NULL,
  `probe_len` INT NULL,
  `min_gc_perc` FLOAT NULL,
  `val_nuc_frame_skip` INT NULL,
  `inval_nuc_frame_skip` TINYINT(1) NULL,
  `computers_pc_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Benchmarks_Computers_idx` (`computers_pc_id` ASC),
  CONSTRAINT `fk_Benchmarks_Computers`
    FOREIGN KEY (`computers_pc_id`)
    REFERENCES `th6_computers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `th6_genbank`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `th6_genbank` ;

CREATE TABLE IF NOT EXISTS `th6_genbank` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `filename` VARCHAR(45) NULL,
  `chromosome` VARCHAR(45) NULL,
  `benchmarks_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_genbank_Benchmarks1_idx` (`benchmarks_id` ASC),
  CONSTRAINT `fk_genbank_Benchmarks1`
    FOREIGN KEY (`benchmarks_id`)
    REFERENCES `th6_benchmarks` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `th6_times`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `th6_times` ;

CREATE TABLE IF NOT EXISTS `th6_times` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `time_total` FLOAT NULL,
  `time_mono` FLOAT NULL,
  `time_di` FLOAT NULL,
  `time_hairpin` FLOAT NULL,
  `time_gc` FLOAT NULL,
  `genbank_id` INT NOT NULL,
  `count_mono_repeat` INT NULL,
  `count_di_repeat` INT NULL,
  `count_hairpin` INT NULL,
  `count_possible` INT NULL,
  `count_total` INT NULL,
  `count_gc` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Times_genbank1_idx` (`genbank_id` ASC),
  CONSTRAINT `fk_Times_genbank1`
    FOREIGN KEY (`genbank_id`)
    REFERENCES `th6_genbank` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
