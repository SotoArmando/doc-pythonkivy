"""
Example of a simple TCP server that is written in (mostly) coroutine
style and uses asyncio.streams.start_server() and
asyncio.streams.open_connection().

Note that running this example starts both the TCP server and client
in the same process.  It listens on port 12345 on 127.0.0.1, so it will
fail if this port is currently in use.
"""

from __future__ import print_function
import sys
import trollius as asyncio
import asyncio.streams
from trollius import From, Return





def main():
    loop = asyncio.get_event_loop()

    # creates a server and starts listening to TCP connections
    server = MyServer()
    #server.start(loop)

    @asyncio.coroutine
    def client():
        reader, writer = yield From(asyncio.streams.open_connection(
            'invetco.dynddns.org', 7002, loop=loop))

        def send(msg):
            print("> " + msg)
            writer.write((msg + '\n').encode("utf-8"))

        def recv():
            msgback = (yield From(reader.readline()))
            msgback = msgback.decode("utf-8").rstrip()
            print("< " + msgback)
            raise Return(msgback)

        # send a line
        send("canConnect:armando")
        msg = yield From(recv())
        
        
        send('<MSG_Request> <Libreria>Lib.MyLib</Libreria><Metodo>exec SP_Clientes</Metodo> <Parametros>'
        +'<commandText>exec SP_Clientes</commandText>'
        +'<strconnection>Data Source=10.0.0.214;Initial Catalog=db_eRX;Persist Security Info=True;User ID=asoto;Password=$a40227587850</strconnection>'
        +'<Token></Token> </Parametros> </MSG_Request>')
        msg = yield From(recv())
        assert msg == 'begin'
        while True:
            msg = yield From(recv())
            if msg == 'end':
                break

        writer.close()
        yield From(asyncio.sleep(0.5))

    # creates a client and connects to our server
    try:
        loop.run_until_complete(client())
        server.stop(loop)
    finally:
        loop.close()


if __name__ == '__main__':
    main()