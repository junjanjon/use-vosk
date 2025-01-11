import vosk
import wave
import time
import json
from logging import getLogger, INFO, StreamHandler, Formatter

logger = getLogger(__name__)
logger.setLevel(INFO)
formatter = Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
handler = StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(INFO)
logger.addHandler(handler)

# 引数の音声ファイル(.wav)に対して、文字起こしした結果をテキストファイル(.txt)に出力する

# モデルファイルのパス
MODEL_PATH = "vosk-model-ja-0.22"
# 1回の音声認識に使うフレーム数
FRAME_SPAN = 4000
# 進捗を表示する間隔
NOTIFY_TIME_INTERVAL = 10

def main(input_filename, output_filename, model_path):
    # モデルファイルのパス
    model = vosk.Model(model_path)
    logger.info(f"Loaded Model: {model_path}")

    # 音声ファイルを開く
    wf = wave.open(input_filename, "rb")
    logger.info(f"Open: {input_filename}")
    all_frames = wf.getnframes()

    # 開始時間を記録
    start_time = time.time()
    # 前回の通知時間を記録
    last_notify_time = start_time
    read_frames = 0

    # 音声認識器を作成
    rec = vosk.KaldiRecognizer(model, wf.getframerate())

    # 音声認識の実行
    results = []
    while True:
        data = wf.readframes(FRAME_SPAN)
        read_frames += FRAME_SPAN
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            json_dict = json.loads(result)
            text = json_dict["text"]
            if text != "":
                results.append(text)
                logger.debug(f"Result: {text}")
        # 進捗を表示
        last_notify_time = print_progress(read_frames, all_frames, start_time, last_notify_time)

    # 結果をテキストファイルに出力
    with open(output_filename, "w") as f:
        for result in results:
            f.write(result + "\n")
    logger.info(f"Output to {output_filename}")

def print_progress(read_frames, all_frames, start_time, last_notify_time):
    if read_frames > all_frames:
        return last_notify_time
    if time.time() - last_notify_time < NOTIFY_TIME_INTERVAL:
        return last_notify_time
    current_time = time.time()
    elapsed_time = current_time - start_time
    progress = (read_frames / all_frames) * 100
    logger.info(f"[{elapsed_time:.1f}s] {progress:.2f}%")
    return current_time


if __name__ == "__main__":
    # 引数を取得する
    import argparse
    parser = argparse.ArgumentParser(
        description="音声ファイル(.wav)に対して、文字起こしした結果をテキストファイル(.txt)に出力する"
    )
    parser.add_argument("-i", "--input_filenme", help="入力ファイルのパス", required=True)
    parser.add_argument("-o", "--output_filename", help="出力ファイルのパス", required=True)
    parser.add_argument("-m", "--model_path", help="モデルファイルのパス", default=MODEL_PATH)
    args = parser.parse_args()
    main(args.input_filenme, args.output_filename, args.model_path)
