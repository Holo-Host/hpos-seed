from pathlib import Path
from PyInstaller import compat
import shutil


a = Analysis(['send_qt.py'], datas=[('send_qt.qml', '.')])
id = 'hpos-seed-send-qt'
pyz = PYZ(a.pure, a.zipped_data)


if compat.is_darwin:
    exe = EXE(pyz,
              a.scripts,
              console=False,
              exclude_binaries=True,
              name=id)

    coll = COLLECT(exe,
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   name=id)

    app = BUNDLE(coll,
                 name='HPOS Seed.app',
                 bundle_identifier='host.holo.' + id)

    shutil.rmtree(Path(DISTPATH, id))
else:
    exe = EXE(pyz,
              a.scripts,
              a.binaries,
              a.zipfiles,
              a.datas,
              console=False,
              name=id,
              upx=True)
