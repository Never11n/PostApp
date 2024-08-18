# PostApp
This is API for creating posts and comments.

## Installation
For building this app you must have Docker
link for install
````
https://www.docker.com/products/docker-desktop/
````
1. ### Clone the repository:
```bash
   git clone https://github.com/never11n/PostApp.git
```
2. ### Run Docker Desktop
3. ### Run application with docker
```bash
   docker-compose up --build
```
Now, you can get application by
````
http://127.0.0.1:8000/api/docs
````
PS.
This API using Google Gemini, that not allowed in couple countries, if your country not in this list
````
ai.google.dev/gemini-api/docs/available-regions
```` 
you need to run application with VPN \
Tests will run automatically with docker container
## Usage
1. When you are in Swagger, you must create a user by 'Register' function
2. After creating a user, you can get token by token function ( token will be used for authorization )
3. When you have got a token, you need to Authorize. Click on Authorize button and put a token
4. Now you can use all functionality of the API
## Technologies
1. Django
2. Django-ninja
3. Celery
4. Redis (as broker for celery)
5. Docker-compose
6. PyTest