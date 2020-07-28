# Gossip Architecture using Python

Gossip Architecture implementation. Client can query and update for the list of movies. Client will connect to front end server and front end server will randomly choose available RM which consists of 3 server. Client couldn't connect if the server is offline and the server can only takes 2 client and if more than that it will return overloaded. The RM will gossiping each other in certain interval in order to maintain concurrency among the server. 

# Methods

Run instantly all the Replica Manager
```
python3 rm1.py rm2.py rm3.py
```

