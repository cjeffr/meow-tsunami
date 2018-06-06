"""
This program connects to the RabbitMQ, pulls out slip, time, model, passes it back to
Do_Stuff.py for processing.
"""

import json
from threading import Thread
import pika
import sys

slip_dict = {}


class RabbitMQInterface(Thread):
    """Super Class to use threading to grab slip in a timely manner (every second)"""
    def __init__(self, queue, rmq):
        """Super class definition"""
        super(RabbitMQInterface, self).__init__()
        self.queue = queue
        self.host = rmq['host'] # goat.host
        self.exchange = rmq['exchange'] # goat.exchange
        self.uid = rmq['uid'] # goat.uid
        self.pw = rmq['pw'] # goat.pw
        self.vhost = rmq['vhost'] # goat.vhost
        self.port = int(rmq['port']) # goat.port
        self.key = rmq['key'] # goat.key

        self.credentials = pika.PlainCredentials(self.uid, self.pw)
        self.params = pika.ConnectionParameters(self.host, self.port, self.vhost, self.credentials)
        self.conn = pika.BlockingConnection(self.params)
        self.ch = self.conn.channel()
        self.ch.exchange_declare(exchange=self.exchange, type='topic', passive=True)
        self.result = self.ch.queue_declare()
        self.queue_name = self.result.method.queue

    def stop(self):
        self.ch.stop_consuming()


    def run(self):
        """
        A function that connects to the RabbitMQ and returns the slip, model and time
        Returns
        -------

        """
        try:


            """Connect to the RabbitMQ, pull out slip, model, time"""
            def callback(ch, method, properties, body):
                """
                Connect to RabbitMQ and extract data needed to run tsunami estimation
                Parameters
                ----------
                ch: channel
                method: method
                properties: properties
                body: json string of slip values

                Returns
                -------
                Returns slip, time in seconds, model

                """
                m_outer = json.loads(body.decode("utf-8"))  # outer message
                time = m_outer['t']
                m_inner = json.loads(m_outer['result'])  # inner message
                slip = m_inner['slip']
                # slip_dict[time] = slip commented out 6/5/18 to see if it was used
                # print(slip_dict)
                self.queue.put((time, slip, method.routing_key))

            ch = self.ch
            ch.exchange_declare(exchange=self.exchange, type='topic', passive=True)
            ch.queue_bind(exchange=self.exchange, queue=self.queue_name, routing_key=self.key)
            ch.basic_consume(callback, queue=self.queue_name, no_ack=True)
            ch.start_consuming()
           # ch.basicCancel(self.queue_name)
        except Exception as CC: #pika.exceptions.ConnectionClosed as CC:
            print('Pika connection closed {}: {}'.format(type(CC), str(CC)))
            self.stop()
            sys.exit(1)

"""Commented out because I'm using it elsewhere, leaving it in for random testing without having to re-write
    the code: 6/28/17
    """
# q = Queue(maxsize=1)
# processstuff = RabbitMQ_interface(q)
# processstuff.start()
# while (True):
#     time, slip, model = q.get()
#     print ("Outputting: %s %s" % (time, slip))
#
#
#
