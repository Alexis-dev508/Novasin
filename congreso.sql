CREATE TABLE tipo_persona(
  `pk_tipo_persona` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `tipo` VARCHAR(45) NOT NULL
);
CREATE TABLE  institucion (
  `pk_institucion` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nombre_ins` VARCHAR(250) NOT NULL
);
CREATE TABLE  sala (
  `pk_sala` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nombre_sal` VARCHAR(250) NOT NULL,
  `capacidad_sal` INT NOT NULL
  );
CREATE TABLE  persona (
  `pk_persona` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nombre_per` VARCHAR(250) NOT NULL,
  `apellido_per` VARCHAR(250) NOT NULL,
  `fk_tipo` INT NOT NULL,
    FOREIGN KEY (fk_tipo) REFERENCES tipo_persona (pk_tipo_persona)
   );

  CREATE TABLE  congresistas (
  `pk_congresista` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `fk_institucion` INT NOT NULL,
  `email_con` VARCHAR(250) NOT NULL,
  `movil_con` VARCHAR(250) NOT NULL,
  `fk_persona` INT NOT NULL,
  `status` TINYINT NOT NULL,
    FOREIGN KEY (fk_persona) REFERENCES persona (pk_persona),
    FOREIGN KEY (fk_institucion) REFERENCES institucion (pk_institucion)
    
   );

   CREATE TABLE  notificaciones (
  `pk_notificacion` INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
  `contenido_not` VARCHAR(500) NOT NULL,
  `fk_congresista` INT NOT NULL,
    FOREIGN KEY (fk_congresista) REFERENCES congresistas (pk_congresista)
    
   );

   CREATE TABLE  autores (
  `pk_autor` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `fk_persona` INT NOT NULL,
    FOREIGN KEY (fk_persona) REFERENCES persona (pk_persona)
    
   );
   CREATE TABLE  trabajos (
  `pk_trabajos` INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
  `titulo_tra` VARCHAR(250) NOT NULL,
  `abstract_tra` TEXT NOT NULL,
  `fk_congresistas` INT NOT NULL,
  `aceptacion_tra` TINYINT NOT NULL,
  `fk_autores` INT NOT NULL,
  FOREIGN KEY (fk_congresistas) REFERENCES congresistas (pk_congresista),
  FOREIGN KEY (`fk_autores`) REFERENCES `autores` (`pk_autor`)
    
   );

   CREATE TABLE  sesiones (
  `pk_sesion` INT NOT NULL AUTO_INCREMENT  PRIMARY KEY ,
  `nombre_ses` VARCHAR(250) NOT NULL,
  `fecha_ses` DATE NOT NULL,
  `hora_ses` TIME NOT NULL,
  `fk_trabajos` INT NOT NULL,
  `fk_sala` INT NOT NULL,
    FOREIGN KEY (`fk_trabajos`) REFERENCES `trabajos` (`pk_trabajos`),
    FOREIGN KEY (`fk_sala`) REFERENCES `sala` (`pk_sala`)
    
   );

CREATE TABLE  trabajos_autores (
  `pk_trabajos_autor` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `fk_autores` INT NOT NULL,
    FOREIGN KEY (`fk_autores`) REFERENCES `autores` (`pk_autor`)
    
   );










































