from threading import Thread
from pymongo import MongoClient
import goat


class SendToMongoDB(Thread):
    """This class is to connect to the MongoDB and pass my tsunami outputs to the database.
       It is a super class to inherit threading"""
    def __init__(self, mdb):
        self.user = mdb['mUser']
        self.mpw = mdb['mpw']
        self.mhost = mdb['mhost']
        self.mdb = mdb['mdb']
        self.mcoll = mdb['mcoll']
        super(SendToMongoDB, self).__init__()

        # connect to the DB and hold onto connection
        mongodb_uri = 'mongodb://%s:%s@%s:%s/%s' % (self.user, self.mpw, self.mhost, self.mdb)
                      #(goat.mUser, goat.mpw, goat.mhost, goat.mport, goat.mdb)
        client = MongoClient(mongodb_uri)
        db = client[self.mdb]
        coll = db[self.mcoll]

        self.client = client
        self.coll = coll

    def store(self, output):
        """Function that passes the tsunami dictionary"""
        result = self.coll.insert_one(output)
        res = result.inserted_id
        print(res)

        """This piece is just for testing that results went into the DB and returns the values
        cursor = coll.find()
        for document in cursor:
            print(document)
            """
