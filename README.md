This code implements virtual group chats.
OS: windows 10.
IDE: PyCharm, version 3.9.
Note that the client-server architecture has two entities: client who consume services, and server who provides services, So the server code needs to be run first in order for the clients code to work.
The client is a user whose interested at group chatting and The server is responsible for managing the group chats, Its services include access to group chats, printing new messages, etc.
At the beginning of any connection, the client receives an opening message with the
following options:
1.Connect to a group chat.
2.Create a group chat.
3.Exit the server.
Following are the requirements for each option:
1. If the client chooses option 1, the server asks for the client name, group ID
and password. In case that the group ID does exist and is valid aswell as the password
matches it, the server connects the client to the relevant group chat.
2. If the client chooses option 2, the server asks the client for its name and a
password, and then it generates a group ID and connects the client to a new group
chat (with the respective group ID and password). The client is then notified what group ID was generated.
3. If the client chooses option 3, the server disconnects the client.
