class s3Upload2:
        """A simple example class"""

        #def __init__(self,filename, Bucketname,time, temp,tempin,tempout,humidity,weight,interval,steps):
        def __init__(self,filename, Bucketname):
          import os
	  import sys
	  import time
	  import datetime
          self.f = filename
          self.b = Bucketname
	  tab="	"
	  steps=60
	  interval=3

   	  while True:
	  	time.sleep(40)
                myfile=open(self.f+"1.csv", "r") 
		lines = myfile.readlines()
                myfile.close()

                L = list()
                i=0
 		f = open(self.f+".txt", 'r+')
                for line in f.readlines():
                        i=i+1
                        L.append(line[line.index(tab):].lstrip())
                        if i == steps:
                              break
                f.close()

                fi = open(self.f+"1.txt", 'w')
                k=0
                for line in xrange(len(L)):
                    k=interval*(line)
                    strl=str(k)+tab+L[line]
                    fi.write(strl)

                fi.close()

 

                import boto
                import ssl
                s3 = boto.connect_s3()
                bucket=s3.get_bucket(self.b, validate=False)
                print(bucket)

                from boto.s3.key import Key
		try:
                 k = Key(bucket)
                 print(k)
                 k.key = self.f+"1.csv"
                 k.content_type = 'text/html'
                 k.set_contents_from_filename(self.f+"1.csv")
                 k.set_acl('public-read')
                 k.key = self.f+"1.txt"
                 k.content_type = 'text/html'
                 k.set_contents_from_filename(self.f+"1.txt")
                 k.set_acl('public-read')
	#	except SSLError, e:
		except:
    			print "Unexpected error:", sys.exc_info()[0]
    			raise
  			if 'timeout' not in exception.message.lower(): # support all timeouts
    			  print ( exception.message)#exception = e
			  sys.exit()
    			  #break
  			if self.listener.on_timeout() == False:
    			  print ( exception.message)#exception = e
			  sys.exit()
    			  #break
  			if self.running is False:
    			  #break
			  sys.exit()
  			conn.close()
  			sleep(self.snooze_time)

def getLastLine(fname, maxLineLength=80):
    fp=file(fname, "r")
    return fp.readlines()[-1]

Bucketname = 'razmere.si'
myfile='DHT'

#x= s3Upload(myfile,Bucketname,time,temp,hum,weight)
x= s3Upload2(myfile,Bucketname)
#print x.t
#print x.tem
#print x.h
