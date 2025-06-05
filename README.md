# Pick Random Movie From Library

## the program

Requires access to the server (at least on first run)
(and if using the VLC url-stream functionality).

After initial run, caches a top-level list of movies/series.

Options are:
```
--type: movies or series
--server: an non-hardcoded url (including http://) for the server.
--verbose: print debug info.
--reload: reload/refresh the initial cache file.
```

## the plan

A minimal client to Jellyfin's RESTful API, where the api key is stored an env. var.

Continue this (fraught) dive into perl scripting.

## references

https://jmshrv.com/posts/jellyfin-api/

