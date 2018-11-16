#!/bin/bash

# Read username and password
read -p "username: " username
read -s -p "password: " password

# Login
if [[ $(curl -w "STATUS:%{http_code}" -s -H "Content-Type: application/json" -X POST -d '{"username": "'$username'", "password": "'$password'"}' -b cookie-jar -c cookie-jar -k https://info3103.cs.unb.ca:24842/signin) =~ .*STATUS:201 ]]; 
then 
    echo "User successfully created"; 
else
    echo "Failed to create user";
fi;

# Get session
if [[ "$(curl -w "STATUS:%{http_code}" -s -i -X GET -c cookie-jar -b cookie-jar -k https://info3103.cs.unb.ca:24842/signin)" =~ .*STATUS:200 ]]; 
then 
    echo "User successfully retrieved"; 
else
    echo "Failed to login user";
fi;

function call() {
    list=$("$@")
    code=$(echo $list | awk -F"STATUS:" '{print $2}')
    json=$(echo $list | awk -F"STATUS:" '{print $1}')
}

call curl -c cookie-jar -w "STATUS:%{http_code}" -s -X GET -b cookie-jar -k https://info3103.cs.unb.ca:24842/users?user=kmasters

# Retrieve users
if [[ $code == "200" ]]; 
then 
    echo "Successfully retrieved users"; 
else
    echo "Failed to retrieve users: $code";
    echo "Failed to retrieve users: $code" >> testing.log;
    echo $json >> testing.log;
fi;

call curl -c cookie-jar -w "STATUS:%{http_code}" -s -X GET -b cookie-jar -k https://info3103.cs.unb.ca:24842/users/kmasters

# Retrieve user
if [[ $code == "200" ]]; 
then 
    echo "Successfully retrieved user"; 
else
    echo "Failed to retrieve user: $code";
    echo "Failed to retrieve user: $code" >> testing.log;
    echo $json >> testing.log;
fi;

call curl -k -c cookie-jar -w "STATUS:%{http_code}" -s -H "Content-Type: application/json" -X PUT -d '{"nickname": "Kyle", "description": "Essentially a test user"}' -b cookie-jar https://info3103.cs.unb.ca:24842/users/kmasters

# Update a user
if [[ $code == "200" ]]; 
then 
    echo "Successfully updated the user"; 
else
    echo "Failed to update the user: $code";
    echo "Failed to update the user: $code" >> testing.log;
    echo $json >> testing.log;
fi;

call curl -c cookie-jar -w "STATUS:%{http_code}" -s -X GET -b cookie-jar -k https://info3103.cs.unb.ca:24842/lists

# Retrieve all lists
if [[ $code == "200" ]]; 
then 
    echo "Successfully retrieved all lists"; 
else
    echo "Failed to retrieve all lists: $code";
    echo "Failed to retrieve the list: $code" >> testing.log;
    echo $json >> testing.log;
fi;

call curl -c cookie-jar -b cookie-jar -w "STATUS:%{http_code}" -s -H "Content-Type: application/json" -X POST -d '{"title": "Aperture Laboratories", "description": "There is testing to be done"}' -k https://info3103.cs.unb.ca:24842/lists

# Create new list
if [[ $code == "201" ]]; 
then 
    echo "Successfully created new list"; 
else
    echo "Failed to create new list: $code";
    echo "Failed to create new list: $code" >> testing.log;
    echo $json >> testing.log;
fi;

# Determine the uri for a list
uri=$(echo $json | python -c "import sys, json; print json.load(sys.stdin)['uri']");

call curl -c cookie-jar -w "STATUS:%{http_code}" -s -X GET -b cookie-jar -k "$uri"

# Retrieve a list
if [[ $code == "200" ]]; 
then 
    echo "Successfully retrieved list"; 
else
    echo "Failed to retrieve list: $code";
    echo "Failed to retrieve list: $code" >> testing.log;
    echo $json >> testing.log;
    echo "At uri: $uri" >> testing.log
fi;

call curl -b cookie-jar -c cookie-jar -w "STATUS:%{http_code}" -s -H "Content-Type: application/json" -X POST -d '{"title": "Test Item, Please Ignore", "description": "The cake is a lie"}' -k "$uri/items"

# Create new item
if [[ $code == "201" ]]
then 
    echo "Successfully created a new item"
else
    echo "Failed to create a new item: $code";
    echo "Failed to create a new item: $code" >> testing.log;
    echo $json >> testing.log;
    echo "At uri: $uri/items" >> testing.log
fi

# Determine the uri for a list
uri=$(echo $json | python -c "import sys, json; print json.load(sys.stdin)['uri']");

call curl -c cookie-jar -w "STATUS:%{http_code}" -s -X GET -b cookie-jar -k "$uri"

# Retrieve an item
if [[ $code == 200 ]]; 
then 
    echo "Successfully retrieved the item"; 
else
    echo "Failed to retrieve an item: $code";
    echo "Failed to retrieve an item: $code" >> testing.log;
    echo $json >> testing.log;
    echo "At uri: $uri" >> testing.log
fi;

call curl -k -c cookie-jar -w "STATUS:%{http_code}" -s -H "Content-Type: application/json" -X PUT -d '{"title": "Testing", "description": "For the people who are, still alive"}' -b cookie-jar "$uri"

# Update an item
if [[ $code == 200 ]]; 
then 
    echo "Successfully updated the item"; 
else
    echo "Failed to update the  item: $code";
    echo "Failed to update the  item: $code" >> testing.log;
    echo $json >> testing.log;
    echo "At uri: $uri" >> testing.log
fi;

call curl -c cookie-jar -w "STATUS:%{http_code}" -s -X DELETE -b cookie-jar -k "$uri"

# Remove an item
if [[ $code == 200 ]]; 
then 
    echo "Successfully removed the item"; 
else
    echo "Failed to remove the  item: $code";
    echo "Failed to remove the  item: $code" >> testing.log;
    echo $json >> testing.log;
    echo "At uri: $uri" >> testing.log
fi;

uri=$(echo $uri | awk -F"/items" '{print $1}')

call curl -c cookie-jar -w "STATUS:%{http_code}" -s -X DELETE -b cookie-jar -k "$uri"

# Remove a list
if [[ $code == "200" ]]; 
then 
    echo "Successfully removed the list"; 
else
    echo "Failed to remove the list: $code";
    echo "Failed to remove the list: $code" >> testing.log;
    echo $json >> testing.log;
fi;

# Logout
if [[ "$(curl -w "STATUS:%{http_code}" -s -i -X DELETE -c cookie-jar -b cookie-jar -k https://info3103.cs.unb.ca:24842/signin)" =~ .*STATUS:200 ]]; 
then 
    echo "User successfully logged out"; 
else
    echo "Failed to logout user";
fi;

# Login Again
if [[ $(curl -w "STATUS:%{http_code}" -s -H "Content-Type: application/json" -X POST -d '{"username": "'$username'", "password": "'$password'"}' -b cookie-jar -c cookie-jar -k https://info3103.cs.unb.ca:24842/signin) =~ .*STATUS:201 ]]; 
then 
    echo "User successfully created"; 
else
    echo "Failed to create user";
fi;

call curl -c cookie-jar -w "STATUS:%{http_code}" -s -X DELETE -b cookie-jar -k https://info3103.cs.unb.ca:24842/users/kmasters

# Delete user
if [[ $code == "200" ]]; 
then 
    echo "Successfully removed the user"; 
else
    echo "Failed to remove the user: $code";
    echo "Failed to remove the user: $code" >> testing.log;
    echo $json >> testing.log;
fi;