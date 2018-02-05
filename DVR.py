from sys import argv
import thread
import time
import socket
import pickle

start_time=time.clock()
graph = {
            'A':{},
            'B':{},
            'C':{},
            'D':{},
            'E':{},
            'F':{},
        }
distance, predecessor = dict(), dict()

def bellmanford(distancevectorgraph):
    while 1:
        for node in graph:
            distance[node], predecessor[node] = float('inf'), None
        distance[routerid] = 0
        time.sleep(3)


        if time.clock()-start_time<20:
            for i in range(len(distancevectorgraph)):
                key = (distancevectorgraph.keys()[i])
                graph[key]=distancevectorgraph[key]
                for j in distancevectorgraph[key]:
                    graph[key][j]=distancevectorgraph[key][j]
                    graph[j][key]=distancevectorgraph[key][j]

        for _ in range(len(graph)-1):
            for u in graph:
                for v in graph[u]:
                    if distance[v] >=distance[u] + graph[u][v]:
                        distance[v], predecessor[v] = distance[u] + graph[u][v],u

        for i in range(len(graph)):
            key=graph.keys()[i]
            if distance[key]==float('inf'):
                predecessor[key]=None
        

        bellkeys = distance.keys()
        for i in range(len(distance)):
            print "Distance to %s: %f" %(bellkeys[i], distance[bellkeys[i]])
        
        print '\n'


        
def client(portno, distancevectorgraph):
    serverName="127.0.0.1"
    while 1:
        try:
            clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        except:
            print "Socket cannot be bound"

        i = 0
        while i < len(portno):
            time.sleep(4)
            sendmessage = {routerid:graph[routerid]}
            clientSocket.sendto(pickle.dumps(sendmessage),(serverName,int(portno[i])))            
            i+=1



def server(portno):
    serverIP="127.0.0.1"
    serverPort=portno

    serverSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    serverSocket.bind((serverIP,serverPort))
    print "Server setup"


    timer_dict = dict()
    for i in range(len(neighbor_list)):
        timer_dict[neighbor_list[i]] = time.clock()

    while 1:
        serverSocket.settimeout(20)
        try:
            message,clientAddress=serverSocket.recvfrom(2048)
            message = pickle.loads(message)
        except:
            print("message not received from all neighbors")
            for i in range(len(neighbor_list)):
                graph[routerid][neighbor_list[i]]=float('inf')
            continue
            
        
        if message.keys()[0] == 'updated':
            mainkey = (message.keys()[0])
            new = message[mainkey]
            key1 = new.keys()[0]
            distancevectorgraph[routerid][key1] = new[key1]
        
        else:
            key = (message.keys()[0])
            rec=message[key]
            for i in rec:
                graph[i][key]=rec[i]
                graph[key][i]=rec[i]
            timer_dict[key] = time.clock()

        
        for i in range(len(neighbor_list)):
            if time.clock() - timer_dict[neighbor_list[i]] > 15:
                change=neighbor_list[i]
                graph[routerid][change]=float('inf')
                graph[change][routerid]=float('inf')
                
                

        


script, routerid, portno, configfile = argv  

print "I am Router " + routerid
print "My port number is " + portno
configfileobj = open(configfile)
numrouters = configfileobj.readline()
print "Number of routers connected: " + numrouters
numrouters = int(numrouters)
distancevectorgraph = {}
distancevectorgraph[routerid] = {}
routerportlist = []
neighbor_list = []

while numrouters > 0:         
    routerinfostr = configfileobj.readline()
    routerinfolist = routerinfostr.split()
    neighbor_list.append(routerinfolist[0])
    routerportlist.append(routerinfolist[2])
    distancevectorgraph[routerid][routerinfolist[0]] = float(routerinfolist[1])
    numrouters = numrouters - 1

print neighbor_list
thread.start_new_thread(server, (int(portno), ))
time.sleep(4)
thread.start_new_thread(client, (routerportlist, distancevectorgraph))
thread.start_new_thread(bellmanford, (distancevectorgraph, ))
while 1:
    pass
