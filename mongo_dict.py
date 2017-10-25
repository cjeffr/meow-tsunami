from threading import Thread

from pymongo import MongoClient

from RunCascadia import goat


class Send_to_MongoDB(Thread):
    """This class is to connect to the MongoDB and pass my tsunami outputs to the database.
       It is a super class to inherit threading"""
    def __init__(self):
        super(Send_to_MongoDB, self).__init__()



    def connect_to_db(self, output):
        """Function that connects to the DB and passes the tsunami dictionary"""
        mongodb_uri = 'mongodb://%s:%s@%s:%s/%s' % (goat.mUser, goat.mpw, goat.mhost, goat.mport, goat.mdb)
        client = MongoClient(mongodb_uri)
        db = client[goat.mdb]
        coll = db[goat.mcoll]
        result = coll.insert_one(output)
        res = result.inserted_id
        print(res)

        """This piece is just for testing that results went into the DB and returns the values
        cursor = coll.find()
        for document in cursor:
            print(document)
            """




