CREATE TABLE IF NOT EXISTS users(
    username VARCHAR(255) NOT NULL,
    screen_name VARCHAR(255),
    PRIMARY KEY(username)
);

CREATE TABLE IF NOT EXISTS lists(
    id INT AUTO_INCREMENT,
    user_name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    FOREIGN KEY(user_name) REFERENCES users(username)
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
