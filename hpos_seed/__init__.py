from twisted.internet.defer import inlineCallbacks
import os
import wormhole


ACK_MESSAGE = b'ack'
APP_ID = 'holo.host/hpos-seed/v1'
DEFAULT_RELAY_URL = 'ws://relay.magic-wormhole.io:4000/v1'


def _relay_url():
    return os.getenv('HPOS_SEED_RELAY_URL', DEFAULT_RELAY_URL)


@inlineCallbacks
def receive(on_wormhole_code, reactor):
    """Allocate wormhole code, wait for sender, and receive incoming data.

    :param on_wormhole_code: callback that runs with allocated wormhole code
                             once it's available
    :param reactor: :mod:`twisted.internet.reactor` object
    :return: data (``hpos-config.json`` contents)
    :rtype: bytes
    """
    w = wormhole.create(APP_ID, _relay_url(), reactor)
    w.allocate_code()

    wormhole_code = yield w.get_code()
    yield on_wormhole_code(wormhole_code)

    data = yield w.get_message()

    yield w.send_message(ACK_MESSAGE)
    yield w.close()

    return data


@inlineCallbacks
def send(wormhole_code, data, reactor):
    """
    Send data over to receiver with matching wormhole code, then wait for ack.

    :param wormhole_code: matching wormhole code
    :param bytes data: data (``hpos-config.json`` contents)
    :param reactor: :py:mod:`twisted.internet.reactor` object
    """
    w = wormhole.create(APP_ID, _relay_url(), reactor)
    w.set_code(wormhole_code)

    yield w.send_message(data)

    ack_message = yield w.get_message()
    assert ack_message == ACK_MESSAGE

    yield w.close()
