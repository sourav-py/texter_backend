# texter: backend

### Index
- [Introduction](https://github.com/sourav-py/texter_backend/tree/main?tab=readme-ov-file#back-end-codebase-for-texter-a-web-socket-based-chat-application)
- [Database design](https://github.com/sourav-py/texter_backend/tree/main?tab=readme-ov-file#database-design)
- [APIs](https://github.com/sourav-py/texter_backend/tree/main?tab=readme-ov-file#apis)
- [Setup](https://github.com/sourav-py/texter_backend/tree/main?tab=readme-ov-file#setup)
- [Issues](https://github.com/sourav-py/texter_backend/tree/main?tab=readme-ov-file#known-issues)
- [Future developments](https://github.com/sourav-py/texter_backend/tree/main?tab=readme-ov-file#future-developments)

#### Back-end codebase for 'texter', a web socket based chat application.
This repository is a `django` project which handles the back-end processes for a web-sockets based chat application.

Following features are leveraged for the application with this project:
- SMS OTP based authentication (token auth.) 
- Web sockets client/server communication
- Managing messages, users, chatrooms and other data.
- Exposing end-points to fetch users' data, messages data, chatrooms data etc.

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
#### Setup

#### Known issues

#### Future developments

