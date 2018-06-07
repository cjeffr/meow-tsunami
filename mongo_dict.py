from threading import Thread
from pymongo import MongoClient
import time


class SendToMongoDB(Thread):
    """This class is to connect to the MongoDB and pass my tsunami outputs to the database.
       It is a super class to inherit threading"""
    def __init__(self, mdb, out_q):
        super(SendToMongoDB, self).__init__()
        self.user = mdb['mUser']
        self.mpw = mdb['mpw']
        self.mhost = mdb['mhost']
        self.mdb = mdb['mdb']
        self.mcoll = mdb['mcoll']
        self.mport = int(mdb['mport'])
        self.q = out_q


        # connect to the DB and hold onto connection
        mongodb_uri = 'mongodb://%s:%s@%s:%s/%s' % (self.user, self.mpw, self.mhost, self.mport, self.mdb)
                      #(goat.mUser, goat.mpw, goat.mhost, goat.mport, goat.mdb)
        client = MongoClient(mongodb_uri)
        db = client[self.mdb]
        coll = db[self.mcoll]

        self.client = client
        self.coll = coll

    def run(self):
        """Function that passes the tsunami dictionary"""
        while True:
            if self.q.qsize() > 10:

                output = self.q.get()
                result = self.coll.insert_one(output)
                res = result.inserted_id
                print("Mongo db inserted id {}".format(res))
                self.q.task_done()
            else:
                time.sleep(.001)
        """This piece is just for testing that results went into the DB and returns the values
        cursor = coll.find()
        for document in cursor:
            print(document)
            """
