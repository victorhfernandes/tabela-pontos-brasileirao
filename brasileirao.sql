DROP DATABASE db_brasileirao;
CREATE DATABASE db_brasileirao;
USE db_brasileirao;

CREATE TABLE tb_estado (
	sg_estado char(2) NOT NULL,
    CONSTRAINT pk_estado
		PRIMARY KEY (sg_estado)
);

CREATE TABLE tb_arena (
	nm_arena varchar(255) NOT NULL,
    sg_estado char(2) NOT NULL,
    CONSTRAINT pk_arena
		PRIMARY KEY (nm_arena),
    CONSTRAINT fk_arena_estado
		FOREIGN KEY (sg_estado)
			REFERENCES tb_estado(sg_estado)
);

CREATE TABLE tb_time (
	nm_time varchar(255) NOT NULL,
	sg_estado char(2) NOT NULL,
    qt_gols int,
    CONSTRAINT pk_time
		PRIMARY KEY (nm_time),
    CONSTRAINT fk_time_estado
		FOREIGN KEY (sg_estado)
			REFERENCES tb_estado(sg_estado)
);

CREATE TABLE tb_tecnico (
	nm_tecnico varchar(255) NOT NULL,
    CONSTRAINT pk_tecnico
		PRIMARY KEY (nm_tecnico)
);

CREATE TABLE tb_jogo (
	cd_jogo int NOT NULL AUTO_INCREMENT,
    cd_rodada int NOT NULL,
    dt_jogo DATETIME NOT NULL,
    time_mandante varchar(255) NOT NULL,
    time_visitante varchar(255) NOT NULL,
    formacao_mandante varchar(255),
    formacao_visitante varchar(15),
	tecnico_mandante varchar(255),
    tecnico_visitante varchar(255),
    nm_arena varchar(255) NOT NULL,
    placar_mandante int NOT NULL,
    placar_visitante int NOT NULL,
    CONSTRAINT pk_jogo
		PRIMARY KEY (cd_jogo),
	CONSTRAINT fk_time_mandante_jogo
		FOREIGN KEY (time_mandante)
			REFERENCES tb_time(nm_time),
	CONSTRAINT fk_time_visitante_jogo
		FOREIGN KEY (time_visitante)
			REFERENCES tb_time(nm_time),
	CONSTRAINT fk_tecnico_mandante_jogo
		FOREIGN KEY (tecnico_mandante)
			REFERENCES tb_tecnico(nm_tecnico),
	CONSTRAINT fk_tecnico_visitante_jogo
		FOREIGN KEY (tecnico_visitante)
			REFERENCES tb_tecnico(nm_tecnico)
);

CREATE TABLE tb_pontos (
	cd_ano int NOT NULL,
    nm_time varchar(255) NOT NULL,
    qt_pontos int,
    qt_vitorias_casa int,
    qt_vitorias_fora int,
    qt_empates int,
    qt_gols int,
    CONSTRAINT pk_pontos
		PRIMARY KEY (cd_ano, nm_time),
    CONSTRAINT fk_pontos_time
		FOREIGN KEY (nm_time)
			REFERENCES tb_time(nm_time)
);