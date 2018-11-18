#!/bin/bash

# Clear log
echo "Logs for session $(date)" > testing.log

# Track successful tests
count=0
validJson=0
total=0
current=0
prev=0

# Define some colors, pretty!
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Allow parseJson script to run
chmod +x parseJson.py

# Read username and password
read -p "username: " username
read -s -p "password: " password

# Insert line after password
printf "\n"

# Parse data from curl requests
function call() {
    list=$("$@")
    code=$(echo $list | awk -F"STATUS:" '{print $2}')
    json=$(echo $list | awk -F"STATUS:" '{print $1}')
}

# Validation json responses against expected json
function verifyJSON() {
    file="$2.json"
    expected=$(<$file)
    expected=$(printf '%s' "$expected" | sed 's/[0-9]//g')
    actual=$(printf '%s' "$1" | sed 's/[0-9]//g')
    if [[ "$actual" == *"$expected"* ]]
    then
        validJson=$((validJson+1))
    else
        writeError "JSON object failed to validate: $2"
        echo "JSON object failed to validate: $2" >> testing.log
        echo "Actual: " >> testing.log
        echo $actual >> testing.log
        echo "Expected: " >> testing.log
        echo $expected >> testing.log
    fi;
}

function statusUpdate() {
    curTotal=$((total-prevTotal))
    curCount=$((count-prevCount))
    if [ $total -ne 0 ]
    then
        if [ $curTotal -eq $curCount ]
        then
            printf "[${GREEN}PASS${NC}] "
        else
            printf "[${RED}FAIL${NC}] "
        fi;

        echo "$curCount out of $curTotal tests passed"
    fi;
    echo "==[$1]=="
    prevTotal=$total
    prevCount=$count
}

function writeError() {
    printf "[${RED}ERROR${NC}] "
    echo "$1"
}

# Status update
statusUpdate "Signin"

# Login
call curl -w "STATUS:%{http_code}" -s -H "Content-Type: application/json" -X POST -d '{"username": "'$username'", "password": "'$password'"}' -b cookie-jar -c cookie-jar -k https://info3103.cs.unb.ca:24842/signin

if [[ $code == "201" ]]; 
then 
    count=$((count+1))
    verifyJSON "$json" "postSignin"
else
    writeError "Failed to create user";
fi;
total=$((total+1))

# Get session
call curl -w "STATUS:%{http_code}" -s -X GET -c cookie-jar -b cookie-jar -k https://info3103.cs.unb.ca:24842/signin

if [[ $code == "200" ]]; 
then 
    count=$((count+1))
    verifyJSON "$json" "getSignin"
else
    writeError "Failed to login user";
fi;
total=$((total+1))

# Status update
statusUpdate "Users"

# Retrieve users
call curl -c cookie-jar -w "STATUS:%{http_code}" -s -X GET -b cookie-jar -k https://info3103.cs.unb.ca:24842/users?user=kmasters

if [[ $code == "200" ]]; 
then
    count=$((count+1))
    verifyJSON "$json" "getUsers"
else
    writeError "Failed to retrieve users: $code";
    echo "Failed to retrieve users: $code" >> testing.log;
    echo $json >> testing.log;
fi;
total=$((total+1))

# Update a user
call curl -k -c cookie-jar -w "STATUS:%{http_code}" -s -H "Content-Type: application/json" -X PUT -d '{"nickname": "Kyle"}' -b cookie-jar https://info3103.cs.unb.ca:24842/users/kmasters

if [[ $code == "200" ]]; 
then
    count=$((count+1)) 
    verifyJSON "$json" "putUser"
else
    writeError "Failed to update the user: $code";
    echo "Failed to update the user: $code" >> testing.log;
    echo $json >> testing.log;
fi;
total=$((total+1))

# Status update
statusUpdate "Lists"

# Create new list
call curl -c cookie-jar -b cookie-jar -w "STATUS:%{http_code}" -s -H "Content-Type: application/json" -X POST -d '{"title": "Aperture Laboratories", "description": "There is testing to be done"}' -k https://info3103.cs.unb.ca:24842/lists

if [[ $code == "201" ]]; 
then 
    count=$((count+1)) 
    verifyJSON "$json" "postLists" 
else
    writeError "Failed to create new list: $code";
    echo "Failed to create new list: $code" >> testing.log;
    echo $json >> testing.log;
fi;
total=$((total+1))

# Parse out the uri for the new list
uri=$(echo $json | ./parseJson.py "uri");

# Retrieve all lists
call curl -c cookie-jar -w "STATUS:%{http_code}" -s -X GET -b cookie-jar -k https://info3103.cs.unb.ca:24842/lists

if [[ $code == "200" ]]; 
then 
    count=$((count+1)) 
    verifyJSON "$json" "getLists"
else
    writeError "Failed to retrieve all lists: $code";
    echo "Failed to retrieve the list: $code" >> testing.log;
    echo $json >> testing.log;
fi;
total=$((total+1))

# Retrieve a list
call curl -c cookie-jar -w "STATUS:%{http_code}" -s -X GET -b cookie-jar -k "$uri"

if [[ $code == "200" ]]; 
then 
    count=$((count+1)) 
    verifyJSON "$json" "getList"
else
    writeError "Failed to retrieve list: $code";
    echo "Failed to retrieve list: $code" >> testing.log;
    echo $json >> testing.log;
    echo "At uri: $uri" >> testing.log
fi;
total=$((total+1))

statusUpdate "Items"

# Create new item
call curl -b cookie-jar -c cookie-jar -w "STATUS:%{http_code}" -s -H "Content-Type: application/json" -X POST -d '{"title": "Test Item, Please Ignore", "description": "The cake is a lie"}' -k "$uri/items"

if [[ $code == "201" ]]
then 
    count=$((count+1)) 
    verifyJSON "$json" "postItems"
else
    writeError "Failed to create a new item: $code";
    echo "Failed to create a new item: $code" >> testing.log;
    echo $json >> testing.log;
    echo "At uri: $uri/items" >> testing.log
fi;
total=$((total+1))

# Parse out the uri for the new item
uri=$(echo $json | ./parseJson.py "uri");

# Retrieve an item
call curl -c cookie-jar -w "STATUS:%{http_code}" -s -X GET -b cookie-jar -k "$uri"

if [[ $code == 200 ]]; 
then 
    count=$((count+1)) 
    verifyJSON "$json" "getItem"
else
    writeError "Failed to retrieve an item: $code";
    echo "Failed to retrieve an item: $code" >> testing.log;
    echo $json >> testing.log;
    echo "At uri: $uri" >> testing.log
fi;
total=$((total+1))

# Update an item
call curl -k -c cookie-jar -w "STATUS:%{http_code}" -s -H "Content-Type: application/json" -X PUT -d '{"title": "Testing", "description": "For the people who are, still alive"}' -b cookie-jar "$uri"

if [[ $code == 200 ]]; 
then 
    count=$((count+1)) 
    verifyJSON "$json" "putItem"
else
    writeError "Failed to update the  item: $code";
    echo "Failed to update the  item: $code" >> testing.log;
    echo $json >> testing.log;
    echo "At uri: $uri" >> testing.log
fi;
total=$((total+1))

statusUpdate "Teardown"

# Remove an item
call curl -c cookie-jar -w "STATUS:%{http_code}" -s -X DELETE -b cookie-jar -k "$uri"

if [[ $code == 200 ]]; 
then 
    count=$((count+1)) 
    verifyJSON "$json" "deleteItem"
else
    writeError "Failed to remove the  item: $code";
    echo "Failed to remove the  item: $code" >> testing.log;
    echo $json >> testing.log;
    echo "At uri: $uri" >> testing.log
fi;
total=$((total+1))

uri=$(echo $uri | awk -F"/items" '{print $1}')

# Remove a list
call curl -c cookie-jar -w "STATUS:%{http_code}" -s -X DELETE -b cookie-jar -k "$uri"

if [[ $code == "200" ]]; 
then 
    count=$((count+1)) 
    verifyJSON "$json" "deleteList"
else
    writeError "Failed to remove the list: $code";
    echo "Failed to remove the list: $code" >> testing.log;
    echo $json >> testing.log;
fi;
total=$((total+1))

# Logout
call curl -w "STATUS:%{http_code}" -s -X DELETE -c cookie-jar -b cookie-jar -k https://info3103.cs.unb.ca:24842/signin

if [[ $code == "200" ]]; 
then 
    count=$((count+1))
    verifyJSON "$json" "deleteSignin"
else
    writeError "Failed to logout user";
fi;
total=$((total+1))

# Login Again
call curl -w "STATUS:%{http_code}" -s -H "Content-Type: application/json" -X POST -d '{"username": "'$username'", "password": "'$password'"}' -b cookie-jar -c cookie-jar -k https://info3103.cs.unb.ca:24842/signin

if [[ $code == "201" ]]; 
then 
    count=$((count+1))
    verifyJSON "$json" "postSignin"
else
    writeError "Failed to create user";
fi;
total=$((total+1))

# Delete user
call curl -c cookie-jar -w "STATUS:%{http_code}" -s -X DELETE -b cookie-jar -k https://info3103.cs.unb.ca:24842/users/kmasters

if [[ $code == "200" ]]; 
then 
    count=$((count+1)) 
    verifyJSON "$json" "deleteUser"
else
    writeError "Failed to remove the user: $code";
    echo "Failed to remove the user: $code" >> testing.log;
    echo $json >> testing.log;
fi;
total=$((total+1))

statusUpdate "Results"

if [ $total -eq $count ]
then
    printf "[${GREEN}PASS${NC}] "
else
    printf "[${RED}FAIL${NC}] "
fi;

echo "$count out of $total tests received successful response codes"

if [ $validJson -eq $total ]
then
    printf "[${GREEN}PASS${NC}] "
else
    printf "[${RED}FAIL${NC}] "
fi;

echo "$validJson tests received expected json responses"