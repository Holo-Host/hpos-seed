from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
import hpos_seed
import sys


@inlineCallbacks
def send_cli():
    try:
        _, wormhole_code, config_path = sys.argv
        with open(config_path, 'rb') as f:
            yield hpos_seed.send(wormhole_code, f.read(), reactor)
        reactor.callLater(0, reactor.stop)
    except ValueError:
        print("Usage: {} <wormhole_code> <config_path>".format(
            sys.argv[0]), file=sys.stderr)
        reactor.callLater(1, reactor.stop)


def main():
    reactor.callLater(0, send_cli)
    reactor.run()


if __name__ == '__main__':
    main()
