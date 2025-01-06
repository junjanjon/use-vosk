# 音声文字起こしツール

音声ファイル(.wav)に対して、文字起こしした結果をテキストファイル(.txt)に出力する。

## 使い方

### モデルをダウンロードする

https://alphacephei.com/vosk/models からモデルをダウンロードする。

vosk-model-ja-0.22 をダウンロードし、このディレクトリに展開している。ほかのモデルを使う場合は、`-m` オプションで指定する。

### ライブラリのインストール

```bash
pip install -r requirements.txt
```

### コマンド実行

```bash
usage: main.py [-h] -i INPUT_FILENME -o OUTPUT_FILENAME [-m MODEL_PATH]

音声ファイル(.wav)に対して、文字起こしした結果をテキストファイル(.txt)に出力する

options:
  -h, --help            show this help message and exit
  -i INPUT_FILENME, --input_filenme INPUT_FILENME
                        入力ファイルのパス
  -o OUTPUT_FILENAME, --output_filename OUTPUT_FILENAME
                        出力ファイルのパス
  -m MODEL_PATH, --model_path MODEL_PATH
                        モデルファイルのパス
```
