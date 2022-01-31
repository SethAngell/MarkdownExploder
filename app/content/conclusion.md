# Conclusion

## Revisiting Our Predictions

### Were micrsoservices the right decision?

### Components

#### Alert Functionality

__Important Commits for future writing__

_Commit 3fff192048e6686358c0393b573e73ffb05db185_
__Alert endpoint rewritten in Python__

The Alert endpoint has now been rewritten completely in Python, using
the Flask Framework and Flask-SocketIO. The Readme found in the /alert
directory details all the information needed to write a new client.

Important Notes:
* This client does not implement the session creating logic. It was
decided that that logic would be moved to the User API. Instead, it
simply expects a `room` value on the `joined` event which should
contain the session key. This can be returned by the Auth service.

_Commit 11586f3f13190c63c6fca5d61173ed1518e5a88d_
__Supabase and database integrated. Considering regression to Websockets__
As of currently:
* Postgres and PGAdmin are running within the `store` directory
* Supabase is running at the `alert` directory
* Supabase is utilizing the `store` database as it's backend
* Nginx is set up to proxy to both services

However, supabase has been a bit of a pain in the ass to set up,
now that it's running, I really like it. However, it does seem like
it may be more overhead than it's worth, especially considering the
auth situation. For that reason, I may try and throw together a MVP
websocket implementation is Flask. If it's something that can be done
in less than ~6 hours, it will be what is used moving foward.
## For future developers

### What I'd do differently

### What can still be done

## Other lessons learned

## Closing thoughts
