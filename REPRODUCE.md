# 复现

本仓库包含复现全部成品所需的源码。在 macOS 上按下面准备好环境，运行 `./reproduce.sh`，即可在 `build/` 中重新生成：

- 24-bit / 48 kHz 母带与五条分轨、MP3
- MusicXML、MuseScore 工程、出版版式总谱 PDF
- 4K 随谱演奏视频（母带级）、4K 封面版视频、1080p 网页版视频

随机演奏偏差、混响都使用固定种子，同一环境下每次生成的结果相同。

## 环境

以下版本经过验证：

| 组件 | 版本 | 说明 |
|---|---|---|
| macOS | 26 | 视频用到系统字体：宋体 Songti SC、Georgia Italic、DIN Alternate |
| Python | 3.13 | `pip install -r requirements.txt` |
| MuseScore Studio | 4.7.6 | 命令行 `mscore`（Homebrew：`brew install --cask musescore`） |
| ffmpeg | 8.0 | 需带 libx264、libmp3lame |
| sfizz | git f5c6e29（2025-03-17） | 需要其中的 `sfizz_render` |

### 采样

| 采样 | 获取 | 放置位置 |
|---|---|---|
| VSCO 2 Community Edition（git 6dd651d） | https://github.com/sgossner/VSCO-2-CE | `~/soundfonts/VSCO-2-CE` |
| Salamander Grand Piano V3（2020-06-02，SFZ+FLAC） | https://freepats.zenvoid.org/Piano/acoustic-grand-piano.html | `~/soundfonts/SalamanderGrandPiano-SFZ+FLAC-V3+20200602` |

位置可以用环境变量 `SOUNDFONTS` 改到别处。

### sfizz_render

```bash
git clone https://github.com/sfztools/sfizz.git ~/sfizz-src
cd ~/sfizz-src && git checkout f5c6e29 && git submodule update --init --recursive
cmake -B build -DCMAKE_BUILD_TYPE=Release -DSFIZZ_RENDER=ON && cmake --build build -j
```

生成的程序在 `~/sfizz-src/build/library/bin/sfizz_render`，也可以用环境变量 `SFIZZ` 指向别处。

## 运行

```bash
pip install -r requirements.txt
./reproduce.sh          # 全部，约 3–5 分钟
./reproduce.sh audio    # 只做音频
./reproduce.sh score    # 只做总谱
./reproduce.sh video    # 只做视频（需要先完成 audio 和 score）
```

## 各步骤

| 步骤 | 脚本 | 产物 |
|---|---|---|
| 作曲 | `source/pieces/hugo_alpine_long.py` | 每个声部的音符、力度、速度变化 |
| 音频 | `source/render.py`（`score.py`、`room.py`） | MIDI → 采样逐声部干声 → 同一房间混响 → 混音 → 母带（−18 LUFS） |
| 总谱 | `source/to_score.py` → MuseScore → `source/engrave.py` | MusicXML、带出版版式的 `.mscz`、PDF |
| 视频 | `source/export_pages.py` → `source/score_video.py` | 谱页与小节坐标 → 4K 随谱视频、封面版、网页版 |
