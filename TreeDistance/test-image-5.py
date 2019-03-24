from PIL import Image, ImageDraw
im = Image.open("image4-1.png")
d = ImageDraw.Draw(im)

captureWidth = 900.0
actualW = 1800.0
w = actualW / captureWidth

captureHeight = 1535.0
actualH = 3070.0
h = actualH / captureHeight

tl = (65 * w, 302.625 * h)
tr = (835 * w, 302.625 * h)
br = (835 * w, 1262.625 * h)
bl = (65 * w, 1262.625 * h)

tl2 = (498.5 * w, 632.625 * h)
tr2 = (798.5 * w, 632.625 * h)
br2 = (798.5 * w, 932.625 * h)
bl2 = (498.5 * w, 932.625 * h)


line_color = (0, 255, 0)

d.line([tl, tr, br, bl, tl], fill=line_color, width=2)
d.line([tl2, tr2, br2, bl2, tl2], fill=line_color, width=2)

d.line([(0,0), (1800, 3070)], fill=line_color, width=2)

im.save("image5-highlight.png")

"""
x1 : 65, y1 : 302.625

x2 : 835, y2 : 1262.625


x1 : 498.5, y1 : 632.625
x2 : 798.5, y2 : 932.625
"""
