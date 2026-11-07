# 雨果 · 阿尔卑斯兰德勒 · 一分钟版 v3（v2：更透亮、重做高潮和结尾；v3：高潮到结尾太突然 → 第 45 小节起连续渐弱 + 连续渐慢，竖琴和钢琴不断流；v4：46–50 s 重写——叹息式下行、Gm6 落在 B♭、A7 上行接入最后一句，中提琴三度平行，竖琴先下后上）；v5：48 s 之后柔和舒适——Gm6 换 Em7、只轻轻放慢、伴奏律动不断）。v1 留在 hugo_alpine_long_v1.py。
# 风格不变：D 大调、3/4 拍 180 BPM（一小节 1 秒），独奏小提琴 + 竖琴 + 钢琴 + 大提琴/中提琴；
# 音域照旧：小提琴最高 A5，竖琴不超过 D5，签名三音封顶 B5。
#   前奏  0–3    竖琴独自拨着山风，弦乐长音铺底
#   A     4–12   原曲主题原样出现
#   A′    13–21  主题变奏，停在属和弦（半终止）
#   B     22–37  B 小调：大提琴先唱，小提琴约德尔式回答；34–37 逐小节推高，
#                第 37 小节一口气收住速度，竖琴从低到高刮上去，把人送上山顶
#   A″    38–49  高潮：小提琴主题 + 中提琴对旋律（三、六度和声）+ 大提琴走动的低音；
#                在利底亚的 Gmaj7#11 上把最高的 A5 停满一小节；之后 Bm → G → Gm6（一点怅然），
#                该回家时却停在属和弦 A7 上，速度慢慢放宽，最后一拍几乎停住——留一口气
#   尾声  50–56  小提琴放慢、放轻，把山顶那句（F#–A–G–E–C#）再说一遍，才真正落到 D；
#                竖琴从下往上铺开 D6/9，钢琴落下系列签名三音，余音收住
# 透亮：混响更短（RT60 2.0 → 1.6 s）、各声部发送量减少；大提琴/中提琴铺底退后；钢琴伴奏和弦更轻；
#       母带去掉 250 Hz 一带的浑浊，3 kHz 稍加清晰度，10 kHz 以上加一点空气感（不碰最高音的音域上限）。
from score import SALAMANDER, VSCO, Note, Part, Piece, chord, humanize, legato, legato_pedal, n, notes, signature

# chord name -> (piano bass, piano chord on beats 2–3, harp ripple of six eighths, cello pad, viola pad)
CHORDS = {
    "D": ("D2", "F#3 A3 D4", "D3 A3 E4 F#4 A4 D4", "D3", "A3"),
    "G/D": ("D2", "G3 B3 D4", "D3 G3 B3 D4 G4 D4", "D3", "G3"),
    "Bm7": ("B1", "F#3 A3 D4", "B2 F#3 A3 D4 F#4 D4", "B2", "F#3"),
    "Bm": ("B1", "F#3 B3 D4", "B2 F#3 B3 D4 F#4 D4", "B2", "F#3"),
    "Em9": ("E2", "G3 D4 F#4", "E3 B3 D4 F#4 G4 D4", "E3", "G3"),
    "Em7": ("E2", "G3 B3 D4", "E3 B3 D4 G4 B4 G4", "E3", "G3"),
    "A7sus4": ("A1", "G3 D4 E4", "A2 E3 G3 D4 E4 G4", "A2", "G3"),
    "A7": ("A1", "G3 C#4 E4", "A2 E3 G3 C#4 E4 G4", "A2", "G3"),
    "Gmaj7#11": ("G1", "F#3 B3 C#4", "G2 D3 F#3 A3 C#4 F#4", "G2", "F#3"),
    "A13": ("A1", "G3 C#4 F#4", "A2 E3 G3 C#4 E4 G4", "A2", "G3"),
    "G": ("G1", "G3 B3 D4", "G2 D3 G3 B3 D4 G4", "G2", "G3"),
    "Gm6": ("G1", "G3 A#3 E4", "G2 D3 A#3 E4 G4 E4", "G2", "A#3"),
    "F#m7": ("F#2", "A3 C#4 E4", "F#2 C#3 A3 C#4 E4 A4", "F#2", "A3"),
    "D/F#": ("F#2", "F#3 A3 D4", "F#2 D3 A3 D4 F#4 D4", "F#2", "A3"),
}

INTRO = ["D", "G/D", "D", "G/D"]                                                  # bars 0–3
A = ["D", "G/D", "Bm7", "Em9", "A7sus4", "Gmaj7#11", "A13", "D", "D"]            # 4–12
A2 = ["D", "G/D", "Bm7", "Em9", "A7sus4", "F#m7", "Bm7", "Em9", "A7"]            # 13–21
B = ["Bm", "G", "Em7", "F#m7", "Bm", "G", "Em7", "A7",
     "D/F#", "G", "Em9", "A7sus4", "Bm", "G", "Em9", "A7"]                        # 22–37
A3 = ["D", "G/D", "Bm7", "Em9", "A7sus4", "Gmaj7#11", "Gmaj7#11", "A13",
      "Bm", "G", "Em7", "A7"]                                                     # 38–49: ends on the dominant
LAST = ["Gmaj7#11", "A13"]                                                        # 50–51: the summit phrase once more
PROG = INTRO + A + A2 + B + A3 + LAST
FINAL = 52  # bar where the closing D6/9 is laid down
BARS = FINAL + 6  # 57 bars; with the broadening at the end, about a minute
CLIMAX_BARS = range(38, 50)
assert len(PROG) == FINAL


def beat(bar: int, b: float = 0.0) -> float:
    return bar * 3 + b


# ── violin: the tune ─────────────────────────────────────────────────────────────────────────────────
THEME = ("A4:1 D5:1 F#5:1 E5:2 D5:1 B4:2 A4:1 G4:1 B4:1 F#5:1 E5:2 D5:1 "
         "F#5:1 A5:2 G5:1 E5:1 C#5:1 D5:6")  # the original nine bars, note for note
VARIATION = ("A4:0.5 B4:0.5 D5:1 F#5:1 E5:1 G5:0.5 E5:0.5 D5:1 B4:1 C#5:0.5 B4:0.5 A4:1 "
             "G4:1 B4:1 E5:1 D5:2 E5:1 C#5:2 A4:1 B4:1 D5:1 F#5:1 E5:1.5 D5:0.5 B4:1 C#5:3")
ANSWER = ("r:12 "  # the cello sings first
          "B4:1 F#5:1 D5:1 E5:2 B4:1 G4:1 E5:1 D5:1 C#5:2 E5:1 "  # yodel-like leaps in reply
          "F#5:2 E5:1 D5:1 B4:1 G4:1 B4:2 E5:1 E5:1 D5:1 A4:1 "
          "B4:1 D5:1 F#5:1 G5:2 F#5:1 E5:1 G5:1 E5:1 C#5:1 E5:1 G5:1")  # climbing back to the dominant
CLIMAX = ("A4:1 D5:1 F#5:1 E5:2 D5:1 B4:2 A4:1 G4:1 B4:1 F#5:1 E5:2 D5:1 "
          "F#5:1 A5:2 A5:3 G5:1 E5:1 C#5:1 "  # a whole bar on the lydian summit
          "F#5:1.5 E5:0.5 D5:1 D5:1 E5:0.5 D5:0.5 B4:1 D5:1.5 B4:1 A4:0.5 A4:1 C#5:1 E5:1")
# v4（用户：46–50 s 再做好一点）：从山顶叹息着下来（Bm），G 上轻轻绕一下，Gm6 落在借来的 B♭ 上，
# A7 上用分解和弦往上走，直接把人送进最后一句的 F#5–A5
LAST_LINE = "F#5:1 A5:2 G5:1 E5:1 C#5:1 D5:22"  # bars 50–56 (held past the end; the master fade closes it): slower, softer, and home at last

def taper(line: list[Note], from_bar: int, step: int) -> list[Note]:
    """v3（用户：高潮到结尾太突然）：from_bar 起每小节力度降 step，让高潮慢慢落下来"""
    return [Note(x.beat, x.dur, x.pitch, x.vel - step * max(0, int(x.beat // 3) - from_bar + 1)) for x in line]


VIOLIN = (legato(notes(beat(4), THEME, 72), overlap=0.08)
          + legato(notes(beat(13), VARIATION, 70), overlap=0.08)
          + legato(notes(beat(22), ANSWER, 74), overlap=0.08)
          + legato(taper(notes(beat(38), CLIMAX, 90), from_bar=46, step=2), overlap=0.1)
          + legato(notes(beat(50), LAST_LINE, 76), overlap=0.1))

# viola: a counter-line in thirds and sixths under the climax
VIOLA_COUNTER = ("F#4:1 A4:1 D5:1 C#5:2 B4:1 G4:2 F#4:1 E4:1 G4:1 D5:1 C#5:2 A4:1 "
                 "C#5:1 E5:2 E5:3 E5:1 C#5:1 A4:1 "
                 "D5:1.5 C#5:0.5 B4:1 B4:1 A4:0.5 B4:0.5 G4:1 B4:1.5 G4:1 E4:0.5 E4:1 A4:1 C#5:1")  # 46–49: thirds under the violin
# cello: a walking bass under the climax
CELLO_WALK = ("D3:1 F#3:1 A3:1 D3:3 B2:1 D3:1 F#3:1 E3:2 D3:1 A2:3 G2:1 B2:1 D3:1 G2:3 "
              "A2:1 C#3:1 E3:1 B2:2 A2:1 G2:1 B2:1 D3:1 E2:1 G2:1 B2:1 A2:3")


# ── piano: the gentle "oom–pah–pah", lighter chords for a clearer texture ─────────────────────────────
def piano_bar(bar: int, name: str, loud: int) -> list[Note]:
    bass, ch, *_ = CHORDS[name]
    b = beat(bar)
    low = [Note(b, 0.9, n(bass), loud + 12)]
    if 38 <= bar < 46:  # octave bass for weight at the top, dropped as the climax settles
        low.append(Note(b, 0.9, n(bass) + 12, loud + 4))
    return low + chord(b + 1, 0.35, ch, loud - 4) + chord(b + 2, 0.35, ch, loud - 10)


def piano_level(bar: int) -> int:
    if 22 <= bar < 30:
        return 34  # stand back while the cello and violin converse
    if 30 <= bar < 38:
        return 36 + (bar - 30)  # crescendo
    if 38 <= bar < 46:
        return 50
    if 46 <= bar < 52:
        return 48 - 2 * (bar - 45)  # v5: a gentler settle, the accompaniment keeps its pulse  # 45 → 33 over five bars: the climax settles
    return 44


PIANO = [x for bar in range(4, FINAL) for x in piano_bar(bar, PROG[bar], piano_level(bar))]  # v5: no held chords before home
PIANO += chord(beat(FINAL), 22.0, "D2 A2 F#3 B3 E4", 52, roll=0.25) + signature(beat(FINAL, 1.5), "D5", per_second=2.2)


# ── harp: the mountain wind ───────────────────────────────────────────────────────────────────────────
def harp_bar(bar: int, name: str) -> list[Note]:
    ripple = CHORDS[name][2].split()
    lift = 8 if name in ("Gmaj7#11", "A13") else 0
    if 22 <= bar < 30:  # broader quarter-note arpeggios under the cello's song
        return [Note(beat(bar, i), 2.0, n(p), 44 - i * 2) for i, p in enumerate(ripple[:3])]
    if bar == 37:  # glissando up into the climax
        run = "A2 C#3 E3 G3 A3 C#4 E4 G4 A4 C#5".split()
        return [Note(beat(bar, i * 0.3), 3.0 - i * 0.3, n(p), 44 + i * 2) for i, p in enumerate(run)]
    if 46 <= bar <= 51:  # the ripples keep flowing but thin out; falling with the melody, rising again on A7
        notes_ = ripple if bar in (49, 50) else list(reversed(ripple))
        return [Note(beat(bar, i * 0.5), 1.5, n(p), 52 - 2 * (bar - 45) - i * 2 + lift) for i, p in enumerate(notes_)]
    base = 46 if bar < 4 else 54 if bar in CLIMAX_BARS else 48
    return [Note(beat(bar, i * 0.5), 1.5, n(p), base - i * 2 + lift) for i, p in enumerate(ripple)]


HARP = [x for bar in range(FINAL) for x in harp_bar(bar, PROG[bar])]
HARP += [Note(beat(FINAL) + i * 0.35, 22.0 - i * 0.35, n(p), 58 - i * 2) for i, p in enumerate("D3 A3 E4 F#4 A4 B4 D5".split())]
HARP += [Note(beat(FINAL + k, 0) + i * 0.5, 1.5, n(p), 40 - 4 * k - i * 2) for k in (1, 2) for i, p in enumerate("D3 A3 E4 F#4 A4 D4".split())]  # v5: the wind keeps blowing softly
HARP += [Note(beat(FINAL, 7.5) + i * 0.3, 9.0, n(p), 38 - i * 2) for i, p in enumerate("F#4 A4 B4 D5".split())]  # last shimmer


# ── low strings: long notes underneath; the cello sings at the start of B; both move in the climax ────
def pad(index: int, start: int, stop: int) -> list[Note]:
    return [Note(beat(bar), 3.0, n(CHORDS[PROG[bar]][index]), 62) for bar in range(start, stop)]


CELLO_SONG = notes(beat(22), "F#3:2 B3:1 D4:2 B3:1 G3:1 E3:1 B3:1 C#4:3", 72)  # bars 22–25
CELLO = legato(pad(3, 0, 22) + CELLO_SONG + pad(3, 26, 38) + notes(beat(38), CELLO_WALK, 70)
               + pad(3, 50, FINAL) + [Note(beat(FINAL), 22.0, n("D3"), 68)])
VIOLA = legato(pad(4, 0, 38) + notes(beat(38), VIOLA_COUNTER, 70) + pad(4, 50, FINAL)
               + [Note(beat(FINAL), 22.0, n("A3"), 64)])

BREATH = ((0, 60), (4, 60), (12, 62), (21, 70), (22, 62), (30, 76), (37, 100), (38, 108), (45, 114), (46, 110),
          (48, 104), (50, 96), (52, 88), (54, 76), (58, 42))  # v3: a long, even diminuendo from bar 45 instead of a drop at 50
VIOLIN_EXPR = ((4, 90), (21, 94), (34, 98), (37, 110), (38, 116), (45, 122), (46, 118), (48, 112), (50, 108),
               (52, 100), (58, 66))


def beats_of(points):
    return tuple((beat(b), v) for b, v in points)


PIECE = Piece(
    key="hugo_alpine_long",
    bpm=180,
    beats=beat(BARS),
    swing=0.5,
    tempo=(
        (beat(37), 170), (beat(37, 2), 160),  # gather breath before the summit
        (beat(38), 180),  # a tempo for the climax
        # v3: one continuous ritardando from bar 46 to home (no near-stop, no snap back)
        # v5（用户：48 s 之后要柔和舒适，不要和前面变化太大）：只轻轻放慢
        (beat(47), 177), (beat(49), 173), (beat(50), 168), (beat(51), 163), (beat(52), 156), (beat(54), 150),
    ),
    room=1.6,
    seconds=61.0,
    fade=3.5,
    balance_active=True,
    parts=(
        Part("violin", f"{VSCO}/SViolinVib.sfz", 0, 0, humanize(tuple(VIOLIN), seed=321, timing=0.035, vel=3), send=0.26, level=1.0,
             expression=beats_of(VIOLIN_EXPR)),
        Part("piano", SALAMANDER, 0, 1, humanize(tuple(PIANO), seed=322, timing=0.025),
             pedal=legato_pedal([beat(b) for b in range(4, FINAL + 1)], beat(BARS) + 3), volume=110, send=0.22, target=-6.5),
        Part("harp", f"{VSCO}/Harp.sfz", 0, 2, humanize(tuple(HARP), seed=323, timing=0.03), pan=84, send=0.32, target=-7.0),
        Part("cello", f"{VSCO}/CelloEnsSusVib.sfz", 0, 3, humanize(tuple(CELLO), seed=324, timing=0.02), pan=46, send=0.24,
             expression=beats_of(BREATH), target=-12.0),
        Part("viola", f"{VSCO}/ViolaEnsSusVib.sfz", 0, 4, humanize(tuple(VIOLA), seed=325, timing=0.02), pan=60, send=0.26,
             expression=beats_of(BREATH), target=-13.0),
    ),
    meta={
        "cn": "雨果 · 一分钟版 v2", "style": "阿尔卑斯兰德勒 · 独奏小提琴 + 竖琴",
        "master_eq": (
            "highpass=f=40,"
            "equalizer=f=250:t=q:w=1.0:g=-2.5,"  # clear the low-mid haze
            "equalizer=f=3000:t=q:w=1.2:g=1.2,"  # a little definition
            "equalizer=f=10000:t=h:w=0.7:g=2.5,"  # air
        ),
    },
)
