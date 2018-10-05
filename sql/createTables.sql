CREATE TABLE IF NOT EXISTS lists(
    id INT AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    description TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS items(
    id INT AUTO_INCREMENT,
    list_id INT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (id) REFERENCES lists(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS access(
    id INT AUTO_INCREMENT,
    list_id INT,
    user_id INT,
    FOREIGN KEY (list_id) REFERENCES lists(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    PRIMARY KEY(id)
);