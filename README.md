# Cale

## Prerequisites

- MongoDB
- python-pymongo
- python-flask

## Mongo Help

Adding a fake user to DB:

```
> use cale
switched to db cale
> db.users.insert({ 'username': 'abc', 'password': 'def' });
WriteResult({ "nInserted" : 1 })
```

Verify Insertion:

```
> db.users.find()
{ "_id" : ObjectId("580ae343fc5f56250f2b3762"), "username" : "abc", "password" : "def" }
```
