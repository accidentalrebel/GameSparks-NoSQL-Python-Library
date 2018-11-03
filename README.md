# GameSparks NoSQL Python Library

A simple python library for managing and editing NoSQL databases in GameSparks.

The library makes use of GameSpark's REST API to manage data in a specified game's MongoDB databases.

## Setting up
Create a `.gs-auth` file and place it in your home folder.

```
{
    "user_name" : "user@email.com",
    "password" : "password",
    "api_key" : "ABCDEFGHIJK"
}
```

## Sample Usage

Here's an example on how to use this library.

```python
import gs_nosql as gs

user_name = 'user'
collection = 'player'

gs.authenticate(False) # Set to True if you want to connect to Live server

def get_gems():
    nosql_params = '{"query": {"userName":"' + user_name + '"}}'
    records = gs.collection_find(collection, nosql_params)
    if records:
        record = records[0]
        gem_count = record['currency1']['$numberLong']
        print('Current gem count: ' + gem_count)

def set_gems(gems_to_set):
    nosql_params = '{"multi": false, "query": {"userName":"' + user_name + '"}, "update": { "$set" : { "currency1" : { "$numberLong":"' + str(gems_to_set) + '" } }}, "upsert": false}'
    gs.collection_update('player', nosql_params)

get_gems()
set_gems(100)

```

Here's what the output looks like:
```
Access token retrieved.
Stage Base URL for PREVIEW retrieved.
JWT Token retrieved.

Current gem count: 15
Successfully updated the collection
```
