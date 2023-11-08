# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata

datas = [('../resources/CLI_LICENSE.rtf', '.'), ('../resources/NOTICE.txt', '.')]
datas += collect_data_files('streamlit')
datas += copy_metadata('streamlit')
datas += collect_data_files('keyrings.alt', include_py_files=True)
datas += copy_metadata('keyrings.alt')
datas += collect_data_files('streamlit_quill')

hidden_imports = ['streamlit.runtime.scriptrunner.magic_funcs']

block_cipher = None

pf_a = Analysis(
    ['pf.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pf_pyz = PYZ(pf_a.pure, pf_a.zipped_data, cipher=block_cipher)
pf_exe = EXE(
    pf_pyz,
    pf_a.scripts,
    [],
    exclude_binaries=True,
    name='pf',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)


pfazure_a = Analysis(
    ['pfazure.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pfazure_pyz = PYZ(pfazure_a.pure, pfazure_a.zipped_data, cipher=block_cipher)
pfazure_exe = EXE(
    pfazure_pyz,
    pfazure_a.scripts,
    [],
    exclude_binaries=True,
    name='pfazure',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    pf_exe,
    pf_a.binaries,
    pf_a.zipfiles,
    pf_a.datas,
    pfazure_exe,
    pfazure_a.binaries,
    pfazure_a.zipfiles,
    pfazure_a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='promptflow',
)