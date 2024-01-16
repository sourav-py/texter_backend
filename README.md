# texter: backend

### Index
- [Introduction](https://github.com/sourav-py/texter_backend/tree/main?tab=readme-ov-file#introduction)
- [Database design](https://github.com/sourav-py/texter_backend/tree/main?tab=readme-ov-file#database-design)
- [APIs](https://github.com/sourav-py/texter_backend/tree/main?tab=readme-ov-file#apis)
- [Authentication](https://github.com/sourav-py/texter_backend/tree/main?tab=readme-ov-file#authentication)
- [Web Sockets](https://github.com/sourav-py/texter_backend/tree/main?tab=readme-ov-file#web-sockets)
- [Setup](https://github.com/sourav-py/texter_backend/tree/main?tab=readme-ov-file#setup)
- [Issues](https://github.com/sourav-py/texter_backend/tree/main?tab=readme-ov-file#known-issues)
- [Future developments](https://github.com/sourav-py/texter_backend/tree/main?tab=readme-ov-file#future-developments)

#### Introduction.
This repository is a `django` project which handles the back-end processes for a web-sockets based chat application, texter.

Following features are leveraged for the application with this project:
- SMS OTP based authentication (token auth.) 
- Web sockets client/server communication
- Managing messages, users, chatrooms and other data.
- Exposing end-points to fetch users' data, messages data, chatrooms data etc.


#### Tech stack:
- [Django](https://www.djangoproject.com/)
- [Django-rest-framework](https://www.django-rest-framework.org/)
- [Django-channels](https://channels.readthedocs.io/)
- [Redis](https://redis.io/) : *Cache to manage web sockets message queue*


#### Database design
![db_design](/media/docs/erd.png)

#### APIs
Authentication
- `/auth/user/`
- `/auth/sendotp/`
- `/auth/verifyotp/`
- `/auth/updateprofile/`
- `/auth/activitystatus/`
- `/auth/fetchuser/`
- `/auth/logout/`

Chat
- `/chat/participation/`
- `/chat/chatrooms/`
- `/chat/messages/`
#### Authentication
Token based authentication flow is implemented with this project where a cookie set on user's browser after succesful verification of users' phone number. Overall flow for the authentication process is as follows:
- User enters their phone number
- A verification code is sent to their number (Twilio)
- User enters the otp
- Back-end verifies the otp, sets a cookie in the response object and sends the response to the client (user's browser)
  
#### Web-Sockets 

#### Setup
- Clone the repository
- Install the dependencies `pip3 install requirements.txt`
- Run the redis server `docker run -p 6379:6379 -d redis:5`
- Run the django server `python3 manage.py runserver`

#### Known issues
- [API endpoints protection](https://github.com/sourav-py/texter_backend/issues/12)
#### Future developments
- [Messages encryption](https://github.com/sourav-py/texter_backend/issues/10)
