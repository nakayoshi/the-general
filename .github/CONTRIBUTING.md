# Contribution Guide

## 使用ライブラリ等

Language
: Python 3.8

Package Manager
: Pipenv

Linter
: PyLint

Formatter
: black

Type Checker
: mypy

## コードの命名規則

基本は、Python のスタイルガイド([PEP-8](https://pep8-ja.readthedocs.io/ja/latest/#id29))に則っています。

- クラス名: PascalCase
- 関数名: snake_case
- 変数名: snake_case
- 定数名: UPPER_CASE
- プライベート関数/変数: \_snake_case

## ディレクトリ構成

- `plugin` 下に、Cog が書かれたクラスの書かれたファイル(Ex: `echo.py`)
  - 書く処理は、`discord.py` とのやりとりを行う部分のみ(メッセージ送受信)
- `logic` 下に、同名のファイルを作成(Ex: `echo.py`)
  - 書く処理は、テキストを受け取って返すまでの部分
- `test` 下に、prefix が `test_` のファイルを作成(Ex: `test_echo.py`)
  - 書く処理は、`logic` 下のファイルのテストを行う部分

```
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── Procfile
├── README.md
├── bot.py
├── logic
│   ├── __init__.py
│   └── echo.py
├── plugin
│   ├── __init__.py
│   └── echo.py
├── requirements.txt
├── runtime.txt
└── tests
    ├── __init__.py
    └── test_echo.py
```

## 型アノテーションについて

mypy での型ヒントチェックを行います。型ヒントはなるべく多く書きましょう。

必須:

- 仮引数
- 関数の返り値

オプション:

- 変数

## 開発環境のセットアップ

1. Pipenv をインストール
1. .env に必要な値を設定 `cp .env-sample .env`
1. 実行 `pipenv run bot`
