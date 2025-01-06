# PyInstallerの設定ファイル
# ビルドプロセスの3つの主要ステップ:
# 1. Analysis - 依存関係の解析とファイル収集
# 2. PYZ - Pythonモジュールのアーカイブ作成
# 3. EXE - 実行可能ファイルの生成

import sys
from pathlib import Path

# ===== 1. 依存関係の解析 =====
a = Analysis(
    # メインスクリプト
    ['main.py'],
    
    # パス設定
    pathex=[
        '.',
        'utils',
        'models',
        'views',
        'config'
    ],
    
    # バイナリとデータファイルの設定
    binaries=[],
    datas=[
        ('config/', 'config/'),  # 設定ファイルを含める
    ],
    
    # 依存関係の設定
    hiddenimports=[
        'utils.aging',
        'models.capsule',
        'models.store',
        'views.dashboard',
        'config.constants'
    ],
    
    # その他の設定
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',  # 不要な大きなライブラリを除外
        'tkinter',
        'test',
        '_pytest'
    ],
    
    # Windows固有の設定
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)

# ===== 2. Pythonモジュールのアーカイブ作成 =====
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None  # 暗号化が必要な場合は設定を変更
)

# ===== 3. 実行可能ファイルの生成 =====
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    
    # アプリケーション設定
    name='CodeCapsule',      # アプリケーション名
    debug=False,              # デバッグモードを無効化
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                # UPX圧縮を有効化
    upx_exclude=[],
    runtime_tmpdir=None,
    
    # 表示設定
    console=False,           # コンソールウィンドウを非表示
    icon=''   # アプリケーションアイコン（存在する場合）
)