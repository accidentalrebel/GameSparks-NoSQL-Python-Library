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
