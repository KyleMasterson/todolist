DELIMITER //

DROP PROCEDURE IF EXISTS login //
DROP PROCEDURE IF EXISTS getLists //
DROP PROCEDURE IF EXISTS createList //
DROP PROCEDURE IF EXISTS getListById //
DROP PROCEDURE IF EXISTS deleteList //
DROP PROCEDURE IF EXISTS createItem //
DROP PROCEDURE IF EXISTS getItem //
DROP PROCEDURE IF EXISTS updateItem //
DROP PROCEDURE IF EXISTS deleteItem //

CREATE PROCEDURE login(IN name VARCHAR(255))
BEGIN
IF EXISTS (SELECT username FROM users WHERE username = name) THEN
  SELECT username FROM users WHERE username = name;
 ELSE
  INSERT INTO users(username) VALUES (name);
 END IF;
END //
  	
CREATE PROCEDURE getLists(IN userID VARCHAR(255))
BEGIN
 SELECT * FROM lists
  where user_name = userID;
END//
	
CREATE PROCEDURE createList(IN userID VARCHAR(255), inTitle VARCHAR(255), inDescription text)
BEGIN
 INSERT INTO lists(user_name, title, description) VALUES (userID, inTitle, inDescription);
 SELECT LAST_INSERT_ID();
END//
	
CREATE PROCEDURE getListById(IN listID INT(11))
BEGIN
 SELECT * FROM items
  WHERE id = list_id;
END//
	
CREATE PROCEDURE deleteList(IN listID INT(11))
BEGIN
 DELETE FROM lists
  WHERE id = listID;
END//

CREATE PROCEDURE createItem(IN listID INT(11), inTitle VARCHAR(255), description text)
BEGIN
 INSERT INTO items(list_id, title, description) VALUES (listID, inTitle, inDescription);
 SELECT LAST_INSERT_ID();
END//

CREATE PROCEDURE getItem(IN itemID INT(11))
BEGIN
 SELECT * FROM items
  WHERE id = itemID;
END//

CREATE PROCEDURE updateItem(IN userID VARCHAR(255), IN itemID INT(11), inTitle VARCHAR(255), inDescription text)
BEGIN
 UPDATE items
  INNER JOIN lists ON items.list_id=lists.id
  SET 
    title = inTitle, 
    description = inDescription
  WHERE id = items.itemID
  AND userID = list_id.username;
END//
	
CREATE PROCEDURE deleteItem(IN itemID INT(11))
BEGIN
 DELETE items.* FROM items
  INNER JOIN lists ON items.list_id=lists.id
  WHERE id = items.itemID
  AND userID = list_id.username;
END//
DELIMITER ;
