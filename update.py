import sys
import time
import socket
import pickle


def client(routers, newCost):
    serverName="127.0.0.1"
    port1=ports[routers[0]]
    port2=ports[routers[1]]


    
    try:
        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    except:
        print "Socket cannot be bound"

    i = 0
    while i < 2:

		if i == 0:
			message = {'updated':{routers[i]:newCost }}
			print message
			clientSocket.sendto(pickle.dumps(message),(serverName,int(port2)))
		else:
			message = {'updated':{routers[i]:newCost}}
			clientSocket.sendto(pickle.dumps(message),(serverName,int(port1)))
			print message
		i+=1


fileA=open('topology/configA.txt','r')
fileB=open('topology/configB.txt','r')
fileC=open('topology/configC.txt','r')
fileD=open('topology/configD.txt','r')
fileE=open('topology/configE.txt','r')
fileF=open('topology/configF.txt','r')

aRouters=fileA.readline()
bRouters=fileB.readline()
cRouters=fileC.readline()
dRouters=fileD.readline()
eRouters=fileE.readline()
fRouters=fileF.readline()

aRouters=int(aRouters)
bRouters=int(bRouters)
cRouters=int(cRouters)
dRouters=int(cRouters)
eRouters=int(eRouters)
fRouters=int(fRouters)


ports= {}


while aRouters>0 or bRouters>0 or cRouters>0 or dRouters>0 or eRouters>0 or fRouters>0:
	
	if aRouters>0:
		aRouters=aRouters-1
		neighboursA=fileA.readline()
		listA=neighboursA.split()
		listA[1]=float(listA[1])
		ports[listA[0]]=int(listA[2])
	if bRouters>0:
		bRouters=bRouters-1
		neighboursB=fileB.readline()
		listB=neighboursB.split()
		listB[1]=float(listB[1])
		ports[listB[0]]=int(listB[2])
	if cRouters>0:
		cRouters=cRouters-1
		neighboursC=fileC.readline()
		listC=neighboursC.split()
		listC[1]=float(listC[1])
		ports[listC[0]]=int(listC[2])
	if dRouters>0:
		dRouters=dRouters-1
		neighboursD=fileD.readline()
		listD=neighboursD.split()
		listD[1]=float(listD[1])
		ports[listD[0]]=int(listD[2])
	if eRouters>0:
		eRouters=eRouters-1
		neighboursE=fileE.readline()
		listE=neighboursE.split()
		listE[1]=float(listE[1])
		ports[listE[0]]=int(listE[2])
	if fRouters>0:
		fRouters=fRouters-1
		neighboursF=fileF.readline()
		listF=neighboursF.split()
		listF[1]=float(listF[1])
		ports[listF[0]]=int(listF[2])

print "Enter routers to edit their connection"
print "Router1 Router2 NewCost"
print '\n'

routers=[]

input = raw_input(">")

input = input.split()

routers.append(input[0])
routers.append(input[1])

client(routers, float(input[2]))

while True:
	del routers[:]
	routers[:] = []

	input = raw_input(">")

	input = input.split()

	routers.append(input[0])
	routers.append(input[1])

	client(routers, float(input[2]))
