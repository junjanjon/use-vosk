#!/bin/bash -xe

SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR

# MP4 ファイルのパスを引数で受け取り、
# ffmpeg で音声を抽出し、
# 音声をテキストに変換するスクリプト

# 引数のファイルパスを取得
MP4_FILE_PATH=$1

if [ -z "${MP4_FILE_PATH}" ]; then
    echo "Usage: $0 <file-path>"
    exit 1
fi

# MP4_FILE_PATH の拡張子の mp4 を wav に置換
WAV_FILE_PATH=${MP4_FILE_PATH//.mp4/.wav}
# MP4_FILE_PATH の拡張子の mp4 を txt に置換
TXT_FILE_PATH=${MP4_FILE_PATH//.mp4/.txt}

python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
# pip install vosk Wave
# pip freeze > requirements.txt

ffmpeg -y -i ${MP4_FILE_PATH} -ab 160k -ac 1 -ar 16000 ${WAV_FILE_PATH}
python ./main.py -i ${WAV_FILE_PATH} -o ${TXT_FILE_PATH}

deactivate
