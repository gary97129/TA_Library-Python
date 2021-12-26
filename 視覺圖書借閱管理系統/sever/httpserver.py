import socketserver, http.server, cgi, socket
import globalvar as gl

count = 0

def re_code():
    global count
    count += 1
    HOST = '127.0.0.1'
    PORT = 7000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(10)
    print(f'\n================== {count} socket start ====================\n')
    print('server start at: %s:%s' % (HOST, PORT))
    print('wait for connection...')

    while True:
        conn, addr = s.accept()
        print('connected by ' + str(addr))
        if gl.get_value('code') == None:
            pass
        else:
        # while True:
            # indata = conn.recv(1024)
            # if len(indata) == 0: # connection closed
            #     conn.close()
            #     print('client closed connection.')
            #     break
            # print('recv: ' + indata.decode())

            # outdata = 'echo ' + indata.decode()
            # conn.send(outdata.encode())

            conn.sendall(gl.get_value('code').encode())
            print('\n==================' + ' '*len(str(count)) + '  socket end  ====================\n')
            gl.set_value('code', None)
        # s.close()
        # conn.close()
        break


class ServerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        http.server.SimpleHTTPRequestHandler.do_GET(self)
 
    def do_POST(self):
        print(self)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        http.server.SimpleHTTPRequestHandler.do_GET(self)
        for key in form.keys(): 
            if key == 'code':
                gl.set_value('code', form[key].value)
                # gl.set_value('code', form[key])
                print(str(count+1) + "：" + str(form[key].value))
        re_code()

PORT = 8000
gl._init()

Handler = ServerHandler
httpd = socketserver.TCPServer(("127.0.0.1", PORT), Handler)

# httpd.socket = ssl.wrap_socket (httpd.socket, 
#         keyfile="path/to/key.pem", 
#         certfile='path/to/cert.pem', server_side=True)


print("serving at port", PORT)
httpd.serve_forever()