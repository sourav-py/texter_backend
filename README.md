# texter: backend
### Back-end codebase for 'texter', a web socket based chat application.
This repository is a `django` project which handles the back-end processes for a web-sockets based chat application. This application offers functionalities including but not limited to - p2p messaging, storing message history, **last seen/online status** of users, and **currently typing indicator**. 
For the front-end  to be able to interact with the back-end, several REST end-points are developed with `django-rest-framework`. 


Following features are leveraged for the application with this project:
- Token based authentication 
- Web sockets client/server communication
- Managing messages, users, chatrooms and other data.
- Exposing end-points to fetch users' data, messages data, chatrooms data etc.

