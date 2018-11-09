CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS lists(
    id INT AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS items(
    id INT AUTO_INCREMENT,
    list_id INT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY (list_id) REFERENCES lists(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    PRIMARY KEY(id)
);
