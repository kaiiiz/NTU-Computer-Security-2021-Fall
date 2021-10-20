CREATE TABLE  IF NOT EXISTS `users` (
    `uid` INT NOT NULL AUTO_INCREMENT,
    `username` TEXT NULL DEFAULT NULL,
    `password` TEXT NULL DEFAULT NULL,
    `flag` TEXT NULL DEFAULT NULL,
    PRIMARY KEY (`uid`)
);

INSERT INTO users (username, password) VALUES ("guest", "guest");

-- INSERT INTO users (username, password, flag) VALUES ("<CENSORED>", "<CENSORED>", "<CENSORED>");
-- INSERT INTO users ... 