DELIMITER //

DROP PROCEDURE IF EXISTS login //
DROP PROCEDURE IF EXISTS getLists //
DROP PROCEDURE IF EXISTS getUser//
DROP PROCEDURE IF EXISTS updateName //
DROP PROCEDURE IF EXISTS createList //
DROP PROCEDURE IF EXISTS getListById //
DROP PROCEDURE IF EXISTS deleteList //
DROP PROCEDURE IF EXISTS createItem //
DROP PROCEDURE IF EXISTS getItemByID //
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

CREATE PROCEDURE getUser(IN name VARCHAR(255))
BEGIN
IF EXISTS (SELECT * FROM users WHERE screen_name = name OR username = name) THEN
 SELECT * FROM users 
  WHERE screen_name = name
    OR username = name;
ELSE
 SELECT * FROM users;
END IF;
END//

CREATE PROCEDURE updateName(IN user VARCHAR(255), name VARCHAR(255))
BEGIN
 UPDATE users
  SET screen_name = name
   WHERE username = user;
END//
	
CREATE PROCEDURE createList(IN userID VARCHAR(255), inTitle VARCHAR(255), inDescription text)
BEGIN
 INSERT INTO lists(user_name, title, description) VALUES (userID, inTitle, inDescription);
 SELECT LAST_INSERT_ID();
END//
	
CREATE PROCEDURE getListById(IN listID INT(11))
BEGIN
 SELECT * FROM lists
  WHERE id = listID;
END//
	
CREATE PROCEDURE deleteList(IN userID VARCHAR(255), IN listID INT(11))
BEGIN
 DELETE lists.* FROM lists
  WHERE id = listID
  AND userID = user_name;
END//

CREATE PROCEDURE createItem(IN listID INT(11), inTitle VARCHAR(255), inDescription text)
BEGIN
 INSERT INTO items(list_id, title, description) VALUES (listID, inTitle, inDescription);
 SELECT LAST_INSERT_ID(), list_id FROM items WHERE list_id = listID;
END//

CREATE PROCEDURE getItemByID(IN itemID INT(11))
BEGIN
 SELECT * FROM items
  WHERE id = itemID;
END//

CREATE PROCEDURE updateItem(IN userID VARCHAR(255), IN itemID INT(11), inTitle VARCHAR(255), inDescription text)
BEGIN
 UPDATE items
  INNER JOIN lists ON items.list_id=lists.id
  SET 
    items.title = inTitle, 
    items.description = inDescription
  WHERE itemID = items.id
  AND userID = lists.user_name;
  SELECT * FROM items WHERE itemID=id;
END//
	
CREATE PROCEDURE deleteItem(IN userID VARCHAR(255), IN itemID INT(11))
BEGIN
 DELETE items.* FROM items
  INNER JOIN lists ON items.list_id=lists.id
  WHERE itemID = items.id
  AND userID = lists.user_name;
END//
DELIMITER ;
