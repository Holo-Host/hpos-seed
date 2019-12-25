from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
import hpos_seed
import sys


def on_wormhole_code(wormhole_code):
    print("Wormhole code:", wormhole_code, file=sys.stderr)


@inlineCallbacks
def receive_cli():
    message = yield hpos_seed.receive(on_wormhole_code, reactor)
    sys.stdout.buffer.write(message)

    reactor.callLater(0, reactor.stop)


def main():
    reactor.callLater(0, receive_cli)
    reactor.run()


if __name__ == '__main__':
    main()
