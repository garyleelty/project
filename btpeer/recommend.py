from btpeer import *
import sys
import os
import json
import random

PEERNAME = "NAME"  # request a peer's canonical id
LISTPEERS = "LIST"
INSERTPEER = "JOIN"
QUERY = "QUER"
QRESPONSE = "RESP"
SENDJSON = "JSON"
PEERQUIT = "QUIT"
REPLY = "REPL"
ERROR = "ERRO"
SEND = "SEND"

class Recommend(BTPeer):

    def __init__(self, maxpeers, serverport, myid=None, serverhost=None):
        # --------------------------------------------------------------------------
        """ Initializes a peer servent (sic.) with the ability to catalog
        information for up to maxpeers number of peers (maxpeers may
        be set to 0 to allow unlimited number of peers), listening on
        a given server port , with a given canonical peer name (id)
        and host address. If not supplied, the host address
        (serverhost) will be determined by attempting to connect to an
        Internet host like Google.
        """
        self.debug = False

        self.maxpeers = int(maxpeers)
        self.serverport = int(serverport)
        if serverhost:
            self.serverhost = serverhost
        else:
            self.__initserverhost()

        if myid:
            self.myid = myid
        else:
            self.myid = '%s:%d' % (self.serverhost, self.serverport)

        self.peerlock = threading.Lock()  # ensure proper access to
        # peers list (maybe better to use
        # threading.RLock (reentrant))
        self.peers = {}  # peerid ==> (host, port) mapping
        self.shutdown = False  # used to stop the main loop

        self.handlers = {"LIST": self.handle_insertpeer,
                         "JSON": self.handle_sendjson,
                         "NAME": self.handle_peername,
                         "QUER": self.handle_query,
                         "RESP": self.handle_qresponse,
                         "QUIT": self.handle_quit
                         }

        for mt in self.handlers:
            self.addhandler(mt, self.handlers[mt])

        self.addrouter(self.router)

    def handle_insertpeer(self,data):
        # --------------------------------------------------------------------------
        """ Handles the INSERTPEER (join) message type. The message data
        should be a string of the form, "peerid  host  port", where peer-id
        is the canonical name of the peer that desires to be added to this
        peer's list of peers, host and port are the necessary data to connect
        to the peer.

        """
        self.peerlock.acquire()

        try:
            try:
                peerid = data.split(" ")[1]
                host = data.split(" ")[2]
                port = data.split(" ")[3]
                peerconn = BTPeerConnection(peerid, host, port, debug=self.debug)
                if self.maxpeersreached():
                    self.__debug('maxpeers %d reached: connection terminating'
                                 % self.maxpeers)
                    peerconn.senddata(ERROR, 'Join: too many peers')
                    return

                # peerid = '%s:%s' % (host,port)
                if peerid not in self.getpeerids() and peerid != self.myid:
                    self.addpeer(peerid, host, port)
                    self.__debug('added peer: %s' % peerid)
                    peerconn.senddata(REPLY, 'Join: peer added: %s' % peerid)
                else:
                    peerconn.senddata(ERROR, 'Join: peer already inserted %s'
                                      % peerid)
            except:
                self.__debug('invalid insert %s: %s' % (str(peerconn), data))
                peerconn.senddata(ERROR, 'Join: incorrect arguments')
        finally:
            self.peerlock.release()

    # end handle_insertpeer method
    def __debug(self, msg):
        print(msg)

    def test(self):
        m1 = 'hello from peer1'
        returns = {}
        self.addhandler('SEND', Recommend.handler1)
        self.connectandsend('3.99.155.154', 1119, 'SEND', m1)

    def receive_type(self, peerid, msg_type, peer_map):
        peer_map[peerid] = msg_type
        print(peer_map)
        return peer_map

    def router(self, peer_map, peerid, msgtype):
        """ Registers a routing function with this peer. The setup of routing
        is as follows: This peer maintains a list of other known peers
        (in self.peers). The routing function should take the name of
        a peer (which may not necessarily be present in self.peers)
        and decide which of the known peers a message should be routed
        to next in order to (hopefully) reach the desired peer. The router
        function should return a tuple of three values: (next-peer-id, host,
        port). If the message cannot be routed, the next-peer-id should be
        None.
        """
        nextids = []
        for i in peer_map:
            if msgtype in peer_map[i] and i != peerid:
                nextids.append(i)
        print("the list of next id is: ")
        print(nextids)
        nextid = random.choice(nextids)
        host, port = BTPeer.getpeer(self,nextid)
        print("The next id and corresponding host and port is:" + str(nextid) + " " + str(host) + " " + str(port))
        return nextid, host, port


    def sendjson(self, speerid, rpeerid):
        bool = 0
        print(rpeerid)
        print(speerid)
        sip_addr = self.getpeer(speerid)
        print(sip_addr)
        rip_addr = self.getpeer(rpeerid)
        print(rip_addr)
        while True:
            if bool == 0:
                print('waiting for file...')
                #ip_addr = ("3.99.155.154", 1119)
                client = socket.socket()
                client.connect(rip_addr)

            def file_put(filedir):
                if os.path.isfile(filedir):
                    file_name = filedir
                    file_size = os.stat(file_name).st_size
                    file_msg = {"action": "put", "name": file_name, "size": file_size}
                    client.send(bytes(json.dumps(file_msg), encoding="utf-8"))
                    print("file name: %s --> file size: %s " % (file_name, file_size))
                    with open(file_name, "rb") as f:
                        for line in f:
                            client.send(line)
                            print("Json file is sent: %s" % len(line))
                        print("File sent finished...")

            if os.path.exists('playlist.json'):
                file_put('playlist.json')
                bool = 1
                break
            else:
                time.sleep(1)  # if file doesn't exist, wait 1s and examine again.

    def handle_sendjson(self):
        while True:
            if os.path.exists('playlist.json' ):
                with open("playlist.json", "rb") as f:
                    data = f.read(2048)
                    print(data)
                break
            elif os.path.exists('recommendation.json' ):
                with open("recommendation.json", "rb") as f:
                    data = f.read(2048)
                    print(data)
                break
            else:
                time.sleep(1)  # if file doesn't exist, wait 1s and examine again.
        return data

    def handle_peername(self, peerconn, data):
        # --------------------------------------------------------------------------
        """ Handles the NAME message type. Message data is not used. """
        peerconn.senddata(REPLY, self.myid)

    # QUERY arguments: "return-peerid key ttl"
    # --------------------------------------------------------------------------
    def handle_query(self, peerconn, data):
        # --------------------------------------------------------------------------
        """ Handles the QUERY message type. The message data should be in the
        format of a string, "return-peer-id  key  ttl", where return-peer-id
        is the name of the peer that initiated the query, key is the (portion
        of the) file name being searched for, and ttl is how many further
        levels of peers this query should be propagated on.

        """
        # self.peerlock.acquire()
        try:
            peerid, key, ttl = data.split()
            peerconn.senddata(REPLY, 'Query ACK: %s' % key)
        except:
            self.__debug('invalid query %s: %s' % (str(peerconn), data))
            peerconn.senddata(ERROR, 'Query: incorrect arguments')
        # self.peerlock.release()

        t = threading.Thread(target=self.__processquery,
                             args=[peerid, key, int(ttl)])
        t.start()

    #
    # --------------------------------------------------------------------------
    def processquery(self, peerid, key, ttl):
        # --------------------------------------------------------------------------
        """ Handles the processing of a query message after it has been
        received and acknowledged, by either replying with a QRESPONSE message
        if the file is found in the local list of files, or propagating the
        message onto all immediate neighbors.

        """
        for fname in self.files.keys():
            if key in fname:
                fpeerid = self.files[fname]
                if not fpeerid:  # local files mapped to None
                    fpeerid = self.myid
                host, port = peerid.split(':')
                # can't use sendtopeer here because peerid is not necessarily
                # an immediate neighbor
                self.connectandsend(host, int(port), QRESPONSE,
                                    '%s %s' % (fname, fpeerid),
                                    pid=peerid)
                return
        # will only reach here if key not found... in which case
        # propagate query to neighbors
        if ttl > 0:
            msgdata = '%s %s %d' % (peerid, key, ttl - 1)
            for nextpid in self.getpeerids():
                self.sendtopeer(nextpid, QUERY, msgdata)

    # --------------------------------------------------------------------------
    def handle_qresponse(self, peerconn, data):
        # --------------------------------------------------------------------------
        """ Handles the QRESPONSE message type. The message data should be
        in the format of a string, "file-name  peer-id", where file-name is
        the file that was queried about and peer-id is the name of the peer
        that has a copy of the file.

        """
        try:
            fname, fpeerid = data.split()
            if fname in self.files:
                self.__debug('Can\'t add duplicate file %s %s' %
                             (fname, fpeerid))
            else:
                self.files[fname] = fpeerid
        except:
            # if self.debug:
            traceback.print_exc()

    def handle_quit(self, peerconn, data):
        # --------------------------------------------------------------------------
        """ Handles the QUIT message type. The message data should be in the
        format of a string, "peer-id", where peer-id is the canonical
        name of the peer that wishes to be unregistered from this
        peer's directory.
        """
        self.peerlock.acquire()
        try:
            peerid = data.lstrip().rstrip()
            if peerid in self.getpeerids():
                msg = 'Quit: peer removed: %s' % peerid
                self.__debug(msg)
                peerconn.senddata(REPLY, msg)
                self.removepeer(peerid)
            else:
                msg = 'Quit: peer not found: %s' % peerid
                self.__debug(msg)
                peerconn.senddata(ERROR, msg)
        finally:
            self.peerlock.release()

    # precondition: may be a good idea to hold the lock before going
    #               into this function
    # --------------------------------------------------------------------------
    def handle_peername(self, peerconn, data):
        # --------------------------------------------------------------------------
        """ Handles the NAME message type. Message data is not used. """
        peerconn.senddata(REPLY, self.myid)

if __name__ == '__main__':
    # read command from stdin
    r = Recommend(0, 1119, serverhost="3.96.179.43")
    read = sys.stdin
    for line in read:
        line = line.strip('\n')
        if line == "":
            continue
        line.split(" ")

        if line.split(" ")[0] == "addpeer":
            r.handle_insertpeer(line)
        if line.split(" ")[0] == "check":
            r.checklivepeers()
        if line.split(" ")[0] == "remove":
            peerid = line.split(" ")[1]
            r.removepeer(peerid)
        if line.split(" ")[0] == "test":
            r.test()
        if line.split(" ")[0] == "get":
            peerid = line.split(" ")[1]
            print(r.getpeer(peerid))
        if line.split(" ")[0] == "send":
            speerid = line.split(" ")[1]
            rpeerid = line.split(" ")[2]
            r.sendjson(speerid, rpeerid)
            #r.recvjson(peerid)
        if line.split(" ")[0] == "type":
            peerid = line.split(" ")[1]
            type = []
            type = line.split(" ")[2:]
            r.receive_type(peerid, type)
        if line.split(" ")[0] == "start":
            peer_number = len(r.peers)
            peer_map = {}
            for i in range(peer_number):
                print("Input the msg type that can be received by peer:" + str(i+1))
                read_type = sys.stdin
                msg_type = []
                for line in read_type:
                    line = line.strip("\n")
                    msg_type = line.split(" ")[:]
                    break
                peer_map = r.receive_type(str(i+1), msg_type, peer_map)
            print("You want to send message from which node?")
            read_sid = sys.stdin
            for line in read_sid:
                line = line.split("\n")
                sid = line[0]
                print(sid)
                break
            print("What type of message you want to send?")
            read_send_type = sys.stdin
            for line in read_send_type:
                line = line.split("\n")
                send_msg_type = line[0]
                print(send_msg_type)
                break
            nextid, host, port = r.router(peer_map, sid, send_msg_type)
            host, port = r.getpeer(sid)
            if send_msg_type in r.handlers:
                msgdata = r.handlers[send_msg_type]
            print(r.handlers[send_msg_type])
            r.sendjson(sid, nextid)
            #r.connectandsend(host, port, send_msg_type, msgdata,
                                       #pid=nextid)
            print("data is sucessfully sent to" + nextid)






