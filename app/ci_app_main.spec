# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['ci_app_main.py'],
             pathex=['F:\\PycharmProjects\\calculator-impact\\app'],
             binaries=[('H:\\Python\\Python39\\envs\\calcapp\\Lib\\site-packages\\PySide2\\plugins\\styles', 'styles'), ('H:\\Python\\Python39\\envs\\calcapp\\Lib\\site-packages\\PySide2\\plugins\\platformthemes', 'platformthemes'), ('H:\\Python\\Python39\\envs\\calcapp\\Lib\\site-packages\\PySide2\\plugins\\platforms', 'platforms')],
             datas=[],
             hiddenimports=['skimage.filters.rank.core_cy_3d'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['PyQt5'],
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
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='ci_app_main')
