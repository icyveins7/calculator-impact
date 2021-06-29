# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['ci_app_main.py'],
             pathex=['F:\\PycharmProjects\\calculator-impact\\app'],
             binaries=[],
             datas=[],
             hiddenimports=['skimage.filters.rank.core_cy_3d'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='ci_app_main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='ci_app_main')
