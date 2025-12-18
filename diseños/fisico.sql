-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Geografia`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Geografia` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Geografia` (
  `ID_ubicacion` INT NOT NULL,
  `nom_ciudad` VARCHAR(45) NULL,
  `longitud` FLOAT NULL,
  `latitud` FLOAT NULL,
  `elevac_estac` FLOAT NULL,
  PRIMARY KEY (`ID_ubicacion`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Tiempo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Tiempo` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Tiempo` (
  `ID_tiempo` INT NOT NULL,
  `año` INT NULL,
  `mes` INT NULL,
  `dia` INT NULL,
  `hora` INT NULL,
  PRIMARY KEY (`ID_tiempo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Hidrologia`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Hidrologia` ;

CREATE TABLE IF NOT EXISTS `mydb`.`Hidrologia` (
  `ID_tiempo` INT NOT NULL,
  `ID_ubicacion` INT NOT NULL,
  `precip_sat` FLOAT NULL,
  `escorrentia_tot` FLOAT NULL,
  `escorrentia_superf` FLOAT NULL,
  `hum_suelo_sat` FLOAT NULL,
  `evap_total` FLOAT NULL,
  `caudal_rio` FLOAT NULL,
  `precip_estac` FLOAT NULL,
  `hum_suelo_estac` FLOAT NULL,
  `temp` FLOAT NULL,
  `vel_viento` FLOAT NULL,
  `hum_rel` FLOAT NULL,
  `presion_estac` FLOAT NULL,
  `inundado` TINYINT NOT NULL,
  PRIMARY KEY (`ID_tiempo`, `ID_ubicacion`),
  INDEX `fk_hidrologia_geologia_idx` (`ID_ubicacion` ASC) VISIBLE,
  CONSTRAINT `fk_hidrologia_geografia`
    FOREIGN KEY (`ID_ubicacion`)
    REFERENCES `mydb`.`Geografia` (`ID_ubicacion`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hidrologia_tiempo`
    FOREIGN KEY (`ID_tiempo`)
    REFERENCES `mydb`.`Tiempo` (`ID_tiempo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
