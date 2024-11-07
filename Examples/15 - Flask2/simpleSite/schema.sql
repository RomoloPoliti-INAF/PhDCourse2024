DROP TABLE IF EXISTS lavoro;
DROP TABLE IF EXISTS example;

CREATE TABLE "lavoro" (
	"id"	integer NOT NULL,
	"lavoro"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "example" (
	"id"	integer NOT NULL,
	"name"	varchar(100) NOT NULL,
	"surname"	varchar(100) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"text"	text NOT NULL,
	"lavoro_id"	bigint NOT NULL,
	FOREIGN KEY("lavoro_id") REFERENCES "lavoro"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);

INSERT INTO "lavoro" ("lavoro") VALUES ('Attore'),('Presentatore'),('Giornalista');