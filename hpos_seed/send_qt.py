from pathlib import Path
from PyQt5.QtCore import QObject, QUrl, pyqtSignal, pyqtSlot
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
from twisted.internet.defer import inlineCallbacks
import hpos_seed
import sys
import wormhole


class App(QObject):
    def __init__(self, qapp, reactor):
        QObject.__init__(self)
        self.qapp = qapp
        self.reactor = reactor

    success = pyqtSignal()

    @pyqtSlot(str, result=str)
    def file_url_name(self, file_url):
        return QUrl(file_url).fileName()

    @pyqtSlot(str, result=bool)
    def is_valid_wormhole_code(self, wormhole_code):
        try:
            wormhole._code.validate_code(wormhole_code)
            return True
        except wormhole.errors.KeyFormatError:
            return False

    @inlineCallbacks
    @pyqtSlot(str, str)
    def send(self, wormhole_code, config_file_url):
        config_path = QUrl(config_file_url).toLocalFile()
        with open(config_path, 'rb') as f:
            yield hpos_seed.send(wormhole_code, f.read(), self.reactor)
            self.success.emit()

    @pyqtSlot()
    def quit(self):
        self.qapp.quit()


def main():
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = Path(__file__).parent

    # https://github.com/kivy/kivy/issues/4182#issuecomment-471488773
    if 'twisted.internet.reactor' in sys.modules:
        del sys.modules['twisted.internet.reactor']

    qapp = QApplication(sys.argv)
    qapp.setApplicationName("HPOS Seed")
    qapp.setOrganizationDomain("holo.host")
    qapp.setOrganizationName("Holo")

    # qt5reactor needs to be imported and installed after QApplication(),
    # but before importing twisted.internet.reactor. See qt5reactor docs.
    import qt5reactor
    qt5reactor.install()

    from twisted.internet import reactor
    app = App(qapp, reactor)

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("app", app)
    engine.load(Path(base_path, 'send_qt.qml').as_uri())

    reactor.run()


if __name__ == '__main__':
    main()
