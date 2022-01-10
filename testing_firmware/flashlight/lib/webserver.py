"""
Very simplistic webserver which serves all files from a specific directory

TODO:
- handle file names and directories more generic
- Maybe HTML output as well?
- Test, test, test
- timeout if nobody is connected after n seconds
"""


import usocket as socket
import os
import ujson as json

class SimpleWebserver(object):
    addr = None
    s = None
    datadir = None

    def __init__(self, datadir):
        self.datadir = datadir

    def serve_index(self, conn):
        files = os.listdir(self.datadir)
        response = dict()
        response["data"] = list()
        for f in files:
            response["data"].append({"name" : f, "url" : '/'+f})

        conn.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
        conn.send(json.dumps(response))

    def serve_file(self, conn, file):
        files = os.listdir(self.datadir)
        if file in files:
            conn.sendall('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
            conn.sendall('[')
            with open(self.datadir + '/'+file, "r") as infile:
                isfirst = True
                for line in infile:
                    if not isfirst:
                        conn.send(",")
                    else:
                        isfirst = False
                    conn.sendall(line)
            conn.sendall(']')



    def serve(self, timeout=10):
        self.addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

        self.s = socket.socket()
        self.s.bind(self.addr)
        self.s.listen(1)
        self.s.settimeout(timeout)

        print('listening on', self.addr)

    def stop_serve(self):
        if self.addr:
            self.s.close()
            self.s = None
            self.addr = None

    def is_running(self):
        return self.addr != None


    def cyclic_handler(self):
        if self.addr:
            cl = None
            addr = None
            try:
                cl, addr = self.s.accept()
            except:
                pass # Timeout -> retry next loop

            if cl: # valid connection
                cl.setblocking(True)
                print('client connected from', addr)
                cl_file = cl.makefile('rwb', 0)
                url = ""
                while True:
                    line = cl_file.readline()
                    #print(line.decode("utf-8"))
                    if line.decode("utf-8").startswith("GET "):
                        get_params = line.decode("utf-8").split(" ")
                        if len(get_params) > 2:
                            url = get_params[1]
                    if not line or line == b'\r\n':
                        break

                if url[1:] in os.listdir(self.datadir):
                    self.serve_file(cl, url[1:])
                else:
                    self.serve_index(cl)
                cl.close()


