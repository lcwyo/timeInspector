# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

specpath = os.path.dirname(os.path.abspath(SPEC))

a = Analysis(['timeInspector.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
a.datas += [('./res/img/logo.ico', '.\\res\img\\logo.ico',  'DATA'),
            ('./res/img/kmf.png','.\\res\img\\kmf.png','DATA'),
            ('./res/img/inspector.png','.\\res\img\\inspector.png','DATA'),
            ('./res/img/ninja.png','.\\res\img\\ninja.png','DATA'),
            ('./res/img/bell.png','.\\res\img\\bell.png','DATA')
            ]   
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='timeInspector',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          #Add an icon to the program.
          icon='.\\res\\img\\logo.ico')
