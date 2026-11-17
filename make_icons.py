# Android simgelerini (minimal at) uretir. Kullanim: python3 make_icons.py [res_klasoru]
import os, sys
from PIL import Image, ImageDraw, ImageFont

RES = sys.argv[1] if len(sys.argv) > 1 else "android/app/src/main/res"
BG = (45, 42, 38, 255)
FG = (245, 236, 218, 255)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
S = 1024

def knight(h):
    f = ImageFont.truetype(FONT, int(h * 1.25))
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    bb = d.textbbox((0, 0), "\u265e", font=f)
    w, hh = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((S - w) / 2 - bb[0], (S - hh) / 2 - bb[1]), "\u265e", font=f, fill=FG)
    return im

dens = {"mdpi": (48, 108), "hdpi": (72, 162), "xhdpi": (96, 216),
        "xxhdpi": (144, 324), "xxxhdpi": (192, 432)}
fg_adapt, fg_legacy = knight(470), knight(560)
bg = Image.new("RGBA", (S, S), BG)

for k, (legacy, adapt) in dens.items():
    d = os.path.join(RES, "mipmap-" + k)
    os.makedirs(d, exist_ok=True)
    fg_adapt.resize((adapt, adapt), Image.LANCZOS).save(os.path.join(d, "ic_launcher_foreground.png"))
    for name, shape in (("ic_launcher.png", "sq"), ("ic_launcher_round.png", "round")):
        m = Image.new("L", (S, S), 0)
        dr = ImageDraw.Draw(m)
        if shape == "sq":
            dr.rounded_rectangle((0, 0, S - 1, S - 1), radius=int(S * .22), fill=255)
        else:
            dr.ellipse((0, 0, S - 1, S - 1), fill=255)
        im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        im.paste(bg, (0, 0), m)
        im.alpha_composite(fg_legacy)
        im.resize((legacy, legacy), Image.LANCZOS).save(os.path.join(d, name))

v = os.path.join(RES, "values")
os.makedirs(v, exist_ok=True)
open(os.path.join(v, "ic_launcher_background.xml"), "w").write(
    '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
    '    <color name="ic_launcher_background">#2D2A26</color>\n</resources>\n')
print("Simgeler uretildi:", RES)
