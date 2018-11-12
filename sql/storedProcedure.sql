DELIMITER //

DROP PROCEDURE IF EXISTS login //
DROP PROCEDURE IF EXISTS createUser //
DROP PROCEDURE IF EXISTS getLists //
DROP PROCEDURE IF EXISTS createList //
DROP PROCEDURE IF EXISTS getListById //
DROP PROCEDURE IF EXISTS deleteList //
DROP PROCEDURE IF EXISTS createItem //
DROP PROCEDURE IF EXISTS getItem //
DROP PROCEDURE IF EXISTS upateItem //
DROP PROCEDURE IF EXISTS deleteItem //

CREATE PROCEDURE login(IN name VARCHAR(255))
BEGIN
 SELECT id FROM users
  WHERE username = name;
END //
   
CREATE PROCEDURE createUser(IN name VARCHAR(255))
BEGIN
 INSERT INTO users(username) VALUES (name);
END//
  	
CREATE PROCEDURE getLists(IN userID int(11))
BEGIN
 SELECT * FROM lists
  where user_id = userID;
END//
	
CREATE PROCEDURE createList(IN userID INT(11), inTitle VARCHAR(255), inDescription text)
BEGIN
 INSERT INTO lists(user_id, title, description) VALUES (userID, inTitle, inDescription);
END//
	
CREATE PROCEDURE getListById(IN listID INT(11))
BEGIN
  SELECT * FROM lists
  WHERE id = listID;
END//
	
CREATE PROCEDURE deleteList(IN listID INT(11))
BEGIN
 DELETE FROM lists
  WHERE id = listID;
END//

CREATE PROCEDURE createItem(IN listID INT(11), inTitle VARCHAR(255), description text)
BEGIN
 INSERT INTO items(list_id, title, description) VALUES (listID, inTitle, inDescription);
END//

CREATE PROCEDURE getItem(IN itemID INT(11))
BEGIN
 SELECT * FROM items
  WHERE id = itemID;
END//

CREATE PROCEDURE updateItem(IN itemID INT(11), inTitle VARCHAR(255), inDescription text)
BEGIN
 UPDATE items title = inTitle, description = inDescription
  WHERE id = itemID;
END//
	
CREATE PROCEDURE deleteItem(IN itemID INT(11))
BEGIN
 DELETE FROM items
  WHERE id = itemID;
END//
DELIMITER ;
