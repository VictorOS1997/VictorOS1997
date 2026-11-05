from PIL import Image, ImageDraw, ImageFont
W, H = 820, 300
BG, BAR, FG, DIM = (26,27,38), (36,40,59), (192,202,245), (86,95,137)
GREEN, BLUE, PURPLE, ORANGE, CYAN = (158,206,106), (122,162,247), (187,154,247), (255,158,100), (125,207,255)
font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 17)
bold = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 17)
script = [
    ("cmd", "whoami"),
    ("out", [("victor", GREEN), (" - data analyst @ ntconsult", FG)]),
    ("cmd", "spark.sql(\"SELECT * FROM accounts\").count()"),
    ("out", [("[ok] ", GREEN), ("big data in, clear answers out", FG)]),
    ("cmd", "model = LGBMRanker().fit(X, y)"),
    ("out", [("[ok] ", GREEN), ("primary account ranked for every user", FG)]),
    ("cmd", "ab_test.run(\"quero_emprestimo\")"),
    ("out", [("[ok] ", GREEN), ("revenue ", FG), ("+40%", GREEN)]),
    ("cmd", "echo $NEXT"),
    ("out", [("data engineering | ML | product analytics", PURPLE)]),
]
def render(lines, typing=None, cursor=True):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    d.rectangle([0,0,W,32], fill=BAR)
    for i,c in enumerate([(247,118,142),(224,175,104),(158,206,106)]):
        d.ellipse([16+i*22,10,28+i*22,22], fill=c)
    d.text((W//2-70,8), "victor@data: ~", font=font, fill=DIM)
    y = 46
    allines = list(lines) + ([("cmd", typing)] if typing is not None else [])
    allines = allines[-12:]
    for kind, content in allines:
        x = 18
        if kind == "cmd":
            d.text((x,y), "$ ", font=bold, fill=CYAN); x += 20
            d.text((x,y), content, font=font, fill=FG); x += d.textlength(content, font=font)
        else:
            for txt, col in content:
                d.text((x,y), txt, font=font, fill=col); x += d.textlength(txt, font=font)
        last_x, last_y = x, y
        y += 21
    if cursor:
        if typing is None: last_x, last_y = 38, y; d.text((18,y), "$ ", font=bold, fill=CYAN)
        d.rectangle([last_x+2, last_y+2, last_x+11, last_y+19], fill=FG)
    return im
frames, durs, done = [], [], []
for kind, content in script:
    if kind == "cmd":
        for k in range(0, len(content)+1, 2):
            frames.append(render(done, content[:k])); durs.append(45)
        done.append((kind, content)); frames.append(render(done)); durs.append(250)
    else:
        done.append((kind, content))
        frames.append(render(done)); durs.append(700)
for blink in range(4):
    frames.append(render(done, cursor=True)); durs.append(500)
    frames.append(render(done, cursor=False)); durs.append(500)
frames[0].save("terminal.gif", save_all=True, append_images=frames[1:], duration=durs, loop=0, optimize=True)
frames[-2].save("preview.png")
print(len(frames), "frames")
