#!/bin/zsh
# 从源码完整复现《云上兰德勒》的全部成品，输出到 build/。
#   ./reproduce.sh            全部
#   ./reproduce.sh audio      只渲染音频（母带 + 分轨 + MP3）
#   ./reproduce.sh score      只生成总谱（MusicXML → MuseScore → PDF）
#   ./reproduce.sh video      只生成视频（需要先有 audio 和 score）
# 环境要求见 REPRODUCE.md。
set -euo pipefail
cd "${0:a:h}"
ROOT=$PWD
B=$ROOT/build
N=Fuer-CN_Laendler-ueber-den-Wolken
PY=${PYTHON:-python3}
MSCORE=${MSCORE:-$(command -v mscore || echo "/Applications/MuseScore 4.app/Contents/MacOS/mscore")}
what=${1:-all}
mkdir -p $B

audio() {
  echo "== 音频：逐声部采样渲染、混响、混音、母带"
  RENDER_OUT=$B/audio $PY source/render.py hugo_alpine_long
  cp $B/audio/hugo_alpine_long.wav $B/${N}_24bit-48kHz.wav
  ffmpeg -loglevel error -y -i $B/${N}_24bit-48kHz.wav -i media/cover.jpg -map 0:a -map 1:v \
    -c:a libmp3lame -b:a 320k -compression_level 0 -ar 48000 -c:v mjpeg -disposition:v attached_pic -id3v2_version 3 \
    -map_metadata -1 -metadata title="云上兰德勒 Ländler über den Wolken" -metadata album="Für CN" -metadata comment="Für CN" \
    -metadata genre="Classical" $B/${N}_320k.mp3
}

score() {
  echo "== 总谱：MusicXML → MuseScore 工程 → 出版版式 → PDF"
  $PY source/to_score.py hugo_alpine_long $B/score
  "$MSCORE" -o $B/${N}.mscz $B/score/hugo_alpine_long.musicxml >/dev/null 2>&1
  $PY source/engrave.py $B/${N}.mscz
  "$MSCORE" -o $B/${N}_score.pdf $B/${N}.mscz >/dev/null 2>&1
  cp $B/score/hugo_alpine_long.musicxml $B/${N}.musicxml
}

video() {
  echo "== 视频：导出谱页与坐标 → 4K 随谱视频（母带级）→ 封面版 → 1080p 网页版"
  $PY source/export_pages.py $B/${N}.mscz $B/pages
  CRF=10 PRESET=slow $PY source/score_video.py $B/pages $B/${N}_24bit-48kHz.wav $B/video all
  mv $B/video/云上兰德勒_演奏过程_4K.mp4 $B/${N}_4K-master.mp4
  mv $B/video/云上兰德勒.mp4 $B/${N}_cover.mp4
  mv $B/video/云上兰德勒_封面.png $B/cover.png
  ffmpeg -loglevel error -y -i $B/${N}_4K-master.mp4 -vf "scale=1920:1080:flags=lanczos" -c:v libx264 -preset slow \
    -crf 20 -maxrate 1500k -bufsize 3000k -g 60 -profile:v high -level 4.1 -pix_fmt yuv420p -c:a aac -b:a 192k \
    -movflags +faststart -map_metadata -1 $B/${N}_1080p-web.mp4
}

case $what in
  audio) audio ;;
  score) score ;;
  video) video ;;
  all) audio; score; video ;;
  *) echo "usage: $0 [all|audio|score|video]" >&2; exit 1 ;;
esac
echo "== 完成，输出在 $B"
ls -la $B
