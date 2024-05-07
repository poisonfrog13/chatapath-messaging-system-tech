# Chatapath 

## Get started here

> Before starting automated testing within 'abra_chatapath' environment, ensure that the file 'abra__olena_gut.postman_environment' is imported.

To ensure smooth testing of all APIs, follow the specified order and authentication procedure:

* **Sign Up:** Create a new user account using the POST Sign Up endpoint. While using an already existing user, such as the admin, is recommended for easier testing with existing data, you can create a new user if necessary. Note that using a new user may require manual intervention for certain operations, like composing a message.

* **Log In:** After signing up or using existing credentials, authenticate with the username and password to obtain a token for accessing protected endpoints.

* **Proceed** to test the remaining APIs, ensuring authentication is maintained throughout the testing process.

When creating a new user via the Sign Up endpoint, use the generated username for logging in to maintain consistency and avoid authentication errors. Upon successful login, you'll receive a response containing the ID of the newly created user. It's crucial to utilize this ID when making subsequent requests, such as composing a message using the **POST** Write Message endpoint. Providing the correct user ID ensures that the message is associated with the correct user account and helps prevent potential data handling errors.

By adhering to this streamlined process and environment setup, you ensure proper authentication for accessing APIs requiring login credentials and facilitate seamless automation of the testing process.

## API schema

| URL | Method | Response | Description |
| ------------- | ------------- |------------- | ------------- |
|/chat/messages| GET | <p>200 – returns a list of messages;<br> 403 – user isn’t authorised<p> | Return all messages|
|/chat/messages?is_unread=true| GET | <p>200 – returns a list of messages;<br> 403 – user isn’t authorised<p> | By default unread=False; if unread=True → return unread messages|
|/chat/messages| POST | <p>201 – a message is written/created;<br> 400 – forbidden user/invalid data;<br> 403 – user isn’t authorised<p> | Write and send a new message |
|/chat/messages/{{int:message_pk}}| GET | <p>200 – returns the message;<br> 403 – user isn’t authorised;<br> 404 – a message doesn’t exist<p> | Read one specific message |
|/chat/messages/{{int:message_pk}}| DELETE | <p>204 – no content (empty string) → a message has been deleted;<br> 403 – user isn’t authorised;<br> 404 – a message doesn’t exist<p> | Delete a specific message |
|/auth/signup| POST | <p>201 – a profile has been created;<br> 400 – invalid data<p> | Create an account |
|/auth/login | POST | <p>200 – successfully signed in;<br> 400 – bad request/invalid data<p> | Log into account |
|/auth/logout | GET | <p>200 – successfully signed out;<br> 401 – user unauthorised<p> | Log out of account |


## Authentication & Authorisation

- Authentication strategy: Token based
- /chat/messages/*
  - Authentication
    - is_auth = True
  - Authorisation 
    - Is_sender = True 
    - Is_receiver = True

## Admin Panel

- Register ChatUser
- Register Message

## Tech Stack

* Django 
* Django REST Framework
* Postman
* Python


## Deployment

* Deploy to Heroku
* Version Control GitHub

