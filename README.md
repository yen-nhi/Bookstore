# Bookstore project
A restful API for a Bookstore   
- apps: 
  + api
- [Database diagram](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1&title=bookstore_db#R7Zttb9s2EIB%2FjT9m0IvtOB9jJ%2Bs6pMVQt1j2yaAlWuJMiRpFxXZ%2F%2FY4SKVmhHKRt9NJNgAGbxyNN8p47nkh74q6i4zuOkvAD8zGdOJZ%2FnLh3E8exrZkFb1JyKiRza1EIAk58pVQJ1uQr1i2VNCM%2BTmuKgjEqSFIXeiyOsSdqMsQ5O9TVdozWvzVBATYEaw9RU%2Fon8UVYSBd6WlL%2BGyZBqL%2FZtlRNhLSyEqQh8tnhTOTeT9wVZ0wUn6LjClO5eHpdina%2FXqgtB8ZxLF7TAH8Kvjx%2Befdx%2F%2Fn957nriN93j4srvcxPiGZqxhNnTqHD5Y5BvzBscVJrMf8nY7riKs0tdQsK9jQBay%2BrevgUqPe8o60WbBnbbzz2hLmugtFun6uDrPhqLXZqo3DSA4koirEayVrVWFD2QkL9B3RimVyRVCBvr0vLkHHyFfQRhSobBFDNhQLOtWoaa9lS9cmxnOofepntZ6IP6FhTfECp0KNhlKIkJdt8fLJhhHhA4iUTgkVK6RASgdcJ8qTOAXxIDkREepDKOpgLfLxod7ukCdwQswgLfgIV1WA2VzZWHnijiocK59LbwnOUNbhIuVBQdl1RBh8UaN8CnW1AB%2FrOHEVy9vE2TfKZW0MVJZyAJeUS7%2FHJ4BMsJXK8ONvjFaOMgzxmBbCE0mciREkQQ5HinWwmTU0g%2FNwqcUR8X%2Fa8TIEREgcPudrdtJJ8UiaTIulbO5pHmRAaYuhhmTASi9yEsyW8YEIr65fZZAZjXUHZrsrwkupcrFgMw0ckBwwD0QcsqV5yJpBA29Lf3gLeF8KSibRC2H0lwm5rBDsGwXlwaxdjkgfkHeNYsqHos2ImpXEmRz2i2DWK895RdM1gGsmkRm2nYJq4cRvPV%2BwqLZbsNg9r%2BNI%2BPnHcm%2FoWXXRbKnwf4F6I%2BEhwzwS%2FNh9oj%2BDpxRzUSA5%2FOCmVYfpiptmUlI7Z5w9ln87i%2B7JP57o13OY%2Fd%2FbZv2jMf1sP2dNh57%2BOmf8KIijun82hisZUZwB%2B03%2Byfm34DcoEbP39A9q%2BaHSBAbhA79m%2BYz6vJtmWkjTc%2BEgMYwdpHsgIa9ewlkfQ%2FdFqPpu%2BXy8%2FDoLSMYL%2FP51i1rtTzMwQzok3jNjdv8jHHjwf09FR%2BnaURe%2BOYqb7HseQXPgbJLo9oO%2FxLkBmU4JEePSB7n2g5L0%2FHzCPW7PEr3xgePG7KaSPCPeH8LRvhO2FgfCb3UcZN13ygioVjONNlo4%2FlOryqkpzdvmkxL5uwK5k8c25cxuu9n%2Fym6rx6qj1aLp4MZo2XB01Ut1eML0xoMYRInQQeI4HHANAtOGWpltE9anj%2BfkGStMD428XfUfSBkDaa7f49kgzfwlNYZk2lEH6Mz69%2FAcQa7rC6Jgxc8Ml6QZ5gjy1emILDzJjUOuDuIb7gW6Jc839E4iDx8jdruOUbmSwJwYbjt47ZnBm2B37AdaHILCGIQtYjOh9JYXly2If%2B2rxKp0HxhK1ZH9jIU7qMARlgtUXFB%2BJeDz7%2FJfsCmxXlO70CUheOOlCDPN9PC%2BctZLFqlle0u2K%2BclJXTSdEqUs4x5%2ByZrqjFYgHuAXze40m51jivL95Pxrv8GmUKz%2BCJnXnf2d1L3%2FFw%3D%3D)
- [System diagram]()

# Table of Contents
- [How to run the project on localhost](#1)
- [Test the api endpoint with OpenAI Swagger user interface](#2)
- [Authorize user](#3)
- [Access admin UI](#4)
- [Run unittest](#5)

## How to run the project on localhost <a name="1"/>
Requirements: 
- python3.8
- git

### Step 1: Clone the project
```git clone https://github.com/yen-nhi/Bookstore.git```

### Step 2: Create a virtual environment
- Install 2 necessary libraries
```
sudo apt install python3-pip
pip install virtualenv
``` 
- Get into inside the project directory 
```
cd Bookstore
```
- Create a virtual environment  
```
python3.8 venv -m venv
```

- Activate the virtual environment  
```
source venv/bin/activate
```

### Step 3: Install requirements packages 

```
pip install -r requirements.txt
```

### Step 4: Config the environments virables 
- In the project directory , create a new file with name ".env"
- Copy the content from ".env.example" to ".env" 
- Change/add your config (optional)

### Step 5: Migrate database
- If you have already a sqlite db or want to store the db in somewhere else, provide the path to the db 
by set an environment virable "DB_PATH" in ".env" file before running the below command.
- Otherwise, if this is the first time running the project without any available database, this below command 
by default will create a sqlite3 database in the project directory
```
python3 manage.py migrate
```
### Step 6: Create superuser for admin operations (optional)
To access the admin page for data checking, you need an admin user
```
python3 manage.py createsuperuser
```
It will ask for email and password and confirm the password, save the user.
![alt text](media/guidelines/create_superuser.png)

### Step 7: Feww..., this is the final step.
Everything is ready, now run the command
```
python3 manage.py runserver
```

## Test the api endpoint with OpenAI Swagger user interface <a name="2"/>
### Create a HTTP request to trigger the api
- Open the browser and redirect to http://localhost:8000/api 

![alt text](media/guidelines/docs_screen.png)

- Click to the endpoint you want to test -> click "**Try it out**" button -> instruction as below image

![alt text](media/guidelines/endpoint_instruction.png)

## Authorize user <a name="3"/>
Some apis need authorization (login). To be authorized, you need to create a user account.
The application has 2 way authorization
- For client server, they have to send an Authorization token in the header, the token can be obtained
from the response when the user login. For example request by cURL command
```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/create-book/' \
  -H 'accept: application/json' \
  -H 'authorization: Token <your_user_token>' \   # Add your authorized token here
  -H 'Content-Type: application/json' \
  -d '{
  "title": "string",
  "author": "string",
  "publish_date": "2023-11-15",
  "ISBN": "string",
  "price": 10
}'
```
- For the swagger UI (the UI we are looking at) use Basic Auth with username and password
    + Create a user
    ![alt text](media/guidelines/register_instruction.png)

  + Authorize user
  ![alt text](media/guidelines/auth.png)
  ![alt text](media/guidelines/auth_user.png)
    
+ After authorize the user, you can test the create, update or delete endpoints.

## Access admin UI <a name="4"/>
- Access http://localhost:8000/admin
- Login with superuser which has created above (see step 6, line 52)

## Run unittest <a name="5"/>
This command will collect all unittest and run them
```
python3 manage.py test
```
