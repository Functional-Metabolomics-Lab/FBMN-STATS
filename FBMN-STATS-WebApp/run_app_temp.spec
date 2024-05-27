# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ("./myenv/Lib/site-packages/altair/vegalite/v5/schema/vega-lite-schema.json","./altair/vegalite/v5/schema/"),
        ("./myenv/Lib/site-packages/streamlit/static", "./streamlit/static"),
        ("./myenv/Lib/site-packages/streamlit/runtime", "./streamlit/runtime"),
        ("./myenv/Lib/site-packages/plotly", "./plotly/"),
	    ("./myenv/Lib/site-packages/pingouin", "./pingouin/"),
        ("./myenv/Lib/site-packages/kaleido", "./kaleido/"),
        ("./myenv/Lib/site-packages/openpyxl", "./openpyxl/"),
        ("./myenv/Lib/site-packages/scikit_posthocs", "./scikit_posthocs/"),
        ("./myenv/Lib/site-packages/gnpsdata", "./gnpsdata/"),
	    ("./myenv/Lib/site-packages/sklearn", "./sklearn/"),
	    ("./myenv/Lib/site-packages/networkx", "./networkx/"),
	    ("./myenv/Lib/site-packages/tabulate", "./tabulate/"),
        ("./myenv/Lib/site-packages/pandas_flavor", "./pandas_flavor/"),
        ("./myenv/Lib/site-packages/numpy", "./numpy/"),
    ],
    hiddenimports=[],
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FBMN-Stats-App',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
