"""
This program connects to the RabbitMQ, pulls out slip, time, model, passes it back to
Do_Stuff.py for processing.
"""

import json
from threading import Thread

import goat

slip_dict = {}


class RabbitMQInterface(Thread):
    """Super Class to use threading to grab slip in a timely manner (every second)"""
    def __init__(self, queue):
        """Super class definition"""
        super(RabbitMQInterface, self).__init__()
        self.queue = queue

    def run(self):
        """
        A function that connects to the RabbitMQ and returns the slip, model and time
        Returns
        -------

        """
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
            m_outer = json.loads(body.decode("utf-8")) # outer message
            time = m_outer['t']
            m_inner = json.loads(m_outer['result']) # inner message
            slip = m_inner['slip']
            slip_dict[time] = slip
            # print(slip_dict)
            self.queue.put((time, slip, method.routing_key))

        channel = goat.Ichannel
        channel.exchange_declare(exchange=goat.Iexchange, type='topic', passive=True)
        channel.queue_bind(exchange=goat.Iexchange, queue=goat.Iqueue_name, routing_key=goat.Ikey)
        channel.basic_consume(callback, queue=goat.Iqueue_name, no_ack=True)
        channel.start_consuming()
        channel.basicCancel(goat.Iqueue_name)


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
