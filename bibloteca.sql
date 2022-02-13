-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema biblioteca
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema biblioteca
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `biblioteca` DEFAULT CHARACTER SET utf8 ;
USE `biblioteca` ;

-- -----------------------------------------------------
-- Table `biblioteca`.`editorial`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `biblioteca`.`editorial` (
  `pk_editorial` SMALLINT(6) NOT NULL AUTO_INCREMENT,
  `nombre_e` VARCHAR(55) NULL,
  PRIMARY KEY (`pk_editorial`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `biblioteca`.`categoria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `biblioteca`.`categoria` (
  `pk_categoria` SMALLINT(6) NOT NULL AUTO_INCREMENT,
  `nombre_c` VARCHAR(50) NULL,
  PRIMARY KEY (`pk_categoria`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `biblioteca`.`subcategoria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `biblioteca`.`subcategoria` (
  `pk_subcategoria` SMALLINT(6) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NULL,
  `fk_categoria` SMALLINT(6) NOT NULL,
  PRIMARY KEY (`pk_subcategoria`),
  INDEX `fk_categoria_idx` (`fk_categoria` ASC) ,
  CONSTRAINT `fk_categoria_s`
    FOREIGN KEY (`fk_categoria`)
    REFERENCES `biblioteca`.`categoria` (`pk_categoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `biblioteca`.`titulo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `biblioteca`.`titulo` (
  `pk_titulo` SMALLINT(6) NOT NULL AUTO_INCREMENT,
  `titulo_n` VARCHAR(85) NULL,
  `isbn` VARCHAR(45) NULL,
  `estatus` SMALLINT(6) NULL,
  `fk_subcategoria` SMALLINT(6) NOT NULL,
  `fk_editorial` SMALLINT(6) NOT NULL,
  PRIMARY KEY (`pk_titulo`),
  INDEX `fk_editorial_idx` (`fk_editorial` ASC) ,
  INDEX `fk_subcategoria_idx` (`fk_subcategoria` ASC) ,
  CONSTRAINT `fk_editorial_t`
    FOREIGN KEY (`fk_editorial`)
    REFERENCES `biblioteca`.`editorial` (`pk_editorial`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_subcategoria_t`
    FOREIGN KEY (`fk_subcategoria`)
    REFERENCES `biblioteca`.`subcategoria` (`pk_subcategoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `biblioteca`.`url`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `biblioteca`.`url` (
  `pk_url` SMALLINT(6) NOT NULL AUTO_INCREMENT,
  `url` TEXT NULL,
  `fk_titulo` SMALLINT(6) NOT NULL,
  `estatus` SMALLINT(6) NULL,
  PRIMARY KEY (`pk_url`),
  INDEX `fk_titulo_idx` (`fk_titulo` ASC) ,
  CONSTRAINT `fk_titulo_u`
    FOREIGN KEY (`fk_titulo`)
    REFERENCES `biblioteca`.`titulo` (`pk_titulo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `biblioteca`.`persona`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `biblioteca`.`persona` (
  `pk_persona` SMALLINT(6) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `apaterno` VARCHAR(45) NULL,
  `amaterno` VARCHAR(45) NULL,
  `sexo` VARCHAR(45) NULL,
  `edad` SMALLINT(6) NULL,
  PRIMARY KEY (`pk_persona`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `biblioteca`.`usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `biblioteca`.`usuario` (
  `pk_usuario` SMALLINT(6) NOT NULL AUTO_INCREMENT,
  `nombre_u` VARCHAR(45) NULL,
  `pssw` VARCHAR(150) NULL,
  `email` VARCHAR(90) NULL,
  `imagen` VARCHAR(250) NULL,
  `fk_persona` SMALLINT(6) NOT NULL,
  PRIMARY KEY (`pk_usuario`),
  INDEX `fk_persona_idx` (`fk_persona` ASC) ,
  CONSTRAINT `fk_persona_us`
    FOREIGN KEY (`fk_persona`)
    REFERENCES `biblioteca`.`persona` (`pk_persona`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `biblioteca`.`evaluacion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `biblioteca`.`evaluacion` (
  `pk_evaluacion` SMALLINT(6) NOT NULL AUTO_INCREMENT,
  `calificacion` SMALLINT(6) NULL,
  `fecha` DATE NULL,
  `fk_titulo` SMALLINT(6) NOT NULL,
  `fk_usuario` SMALLINT(6) NOT NULL,
  `estatus` SMALLINT(6) NULL,
  PRIMARY KEY (`pk_evaluacion`),
  INDEX `fk_titulo_idx` (`fk_titulo` ASC) ,
  INDEX `fk_usuario_idx` (`fk_usuario` ASC) ,
  CONSTRAINT `fk_titulo_e`
    FOREIGN KEY (`fk_titulo`)
    REFERENCES `biblioteca`.`titulo` (`pk_titulo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuario_e`
    FOREIGN KEY (`fk_usuario`)
    REFERENCES `biblioteca`.`usuario` (`pk_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `biblioteca`.`autor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `biblioteca`.`autor` (
  `pk_autor` SMALLINT(6) NOT NULL AUTO_INCREMENT,
  `nombre_a` VARCHAR(85) NULL,
  PRIMARY KEY (`pk_autor`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `biblioteca`.`titulo_autor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `biblioteca`.`titulo_autor` (
  `pk_titulo_autor` SMALLINT(6) NOT NULL AUTO_INCREMENT,
  `fk_titulo` SMALLINT(6) NOT NULL,
  `fk_autor` SMALLINT(6) NOT NULL,
  PRIMARY KEY (`pk_titulo_autor`),
  INDEX `fk_titulo_idx` (`fk_titulo` ASC) ,
  INDEX `fk_autor_idx` (`fk_autor` ASC) ,
  CONSTRAINT `fk_titulo_a`
    FOREIGN KEY (`fk_titulo`)
    REFERENCES `biblioteca`.`titulo` (`pk_titulo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_autor_a`
    FOREIGN KEY (`fk_autor`)
    REFERENCES `biblioteca`.`autor` (`pk_autor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `biblioteca`.`telefono_persona`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `biblioteca`.`telefono_persona` (
  `pk_telefono_persona` SMALLINT(6) NOT NULL AUTO_INCREMENT,
  `telefono` VARCHAR(15) NULL,
  `fk_persona` SMALLINT(6) NOT NULL,
  PRIMARY KEY (`pk_telefono_persona`),
  INDEX `fk_persona_idx` (`fk_persona` ASC) ,
  CONSTRAINT `fk_persona_tel`
    FOREIGN KEY (`fk_persona`)
    REFERENCES `biblioteca`.`persona` (`pk_persona`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
