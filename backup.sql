BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO "alembic_version" VALUES('e8f4b431ce58');
CREATE TABLE users (
	id INTEGER NOT NULL, 
	username VARCHAR(50) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	password VARCHAR(250) NOT NULL, 
	is_admin BOOLEAN NOT NULL, 
	is_active BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
INSERT INTO "users" VALUES(1,'string','user@example.com','$argon2id$v=19$m=65536,t=3,p=4$Yf0zqA379AQ+CILccAlE3g$yZOlGwtg4U/69zhLniT6B2GVQTfGpVlOi/pdw6QmRfM',0,1);
INSERT INTO "users" VALUES(2,'striing','test@example.com','$argon2id$v=19$m=65536,t=3,p=4$GrjIDCBXs0UPFUXa2OyDLA$x8YCWtJBjn6PB5SU0gM8lkvhmNsWS3Gsv6pAhAr114E',0,1);
INSERT INTO "users" VALUES(3,'parth','parth@example.com','$argon2id$v=19$m=65536,t=3,p=4$Ij45pcpqzmflVhNJ31zuXA$ZFodC6IbCVwzqqmAkK+IioMQGu4JKUR4ufbD8ELZlxQ',0,1);
INSERT INTO "users" VALUES(4,'test','test1010@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$0jUK6qoiw6Hb4hQ2qsjzFg$t5NkKwmdQPXkPhOnwDlQkkdSXxGsI4/2yI+9gJpQvcQ',0,0);
COMMIT;
