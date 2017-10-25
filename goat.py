"""
A file to hold all the variables pertaining to Cascadia
"""
#rabbitmq variables
import pika


Ihost = "pc96225.d.cwu.edu"
Iexchange = 'slip-inversion2'
Iuserid = "nif_ro"
Ipassword = "ro"
Ivirtual_host = "/rtgps-products"
Iport = 5672
Ikey = "NA_CAS"

Icredentials = pika.PlainCredentials( Iuserid, Ipassword )
Iparameters = pika.ConnectionParameters( Ihost, Iport, Ivirtual_host, Icredentials )
Iconnection = pika.BlockingConnection( Iparameters )
Ichannel = Iconnection.channel()
Ichannel.exchange_declare( exchange = Iexchange, type = 'topic', passive = True )

Iresult = Ichannel.queue_declare()
Iqueue_name = Iresult.method.queue


#MongoDB credentials
mhost = 'pc96225'
mport = 27018
mUser = 'producer'
mpw = 'Miomyax3'
mdb = 'products'
mcoll = 'tsunami_estimates'
