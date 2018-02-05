# Distance-vector Routing Protocol
Implementation of distance-vector routing protocol using **Bellman-Ford algorithm**.

## Language
- Python

## Usage

### Starting a router

```
python DVR.py <router-id> <port-no> <router-config-file>
```

For example:

```
python DVR.py A 5000 topology/configA.txt
```

### Updating cost of links

```
python update.py
```

## Implementation Details

### Configuration files
The topology map consists of configuration files. Each router has a config file which contains following data:

```
number-of-neighbours
neighbour-1-id neighbour-1-cost neighbour-1-port-no
neighbour-2-id neighbour-2-cost neighbour-2-port-no
.
.
.
neighbour-n-id neighbour-n-cost neighbour-n-port-no
```

For example:

```
2
B 6.5 5001
F 2.2 5005
```

### Format of update packet

Each router shares update packet with its neighbours. Each update packet contains following information:

```
string: router-id
dict: neighbours
```
where neighbours is defined as:

```
string: neighbour-id
float: cost
```

For example:

```
router-id = A
neighbours = {'B' : 6.5 , 'F' : 2.2}
```

### User Datagram Protocol

**UDP** is used as the transport protocol for exchanging link-state packets amongst the neighbours.

### Multi-threading

Each router uses three separate threads for listening (for receiving distance-vector updates), sending (for sending distance-vector updates) and Bellman-Ford calculations (when link cost changes).

### Working

Upon initialization, each router creates a
distance-vector update packet and sends this packet to all direct neighbours.
Upon receiving this distance-vector update packet, each neighbouring router will incorporate the provided information into its routing table. Each router periodically broadcasts the distance-vector update packet to its neighbours every 10 seconds.


On receiving distance-vector update packets from all other routers, a router builds up
a **reachability matrix**. Given a view of the neighbouring routers and their reachability, a
router runs the Bellman-Ford algorithm to compute least-cost paths to all other
routers within the network.

If the cost of a link changes, the connected routers recalculate the cost of reaching other routers and also provide an update to their neighbours, who will then notify their neighbours and so on until the network converges. 



