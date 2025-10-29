import PIL as pil
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def makeCanvas(img):
    width, height = img.size
    canvas = Image.new("RGB", (3*width+6, height+100), (255,255,255))
    return canvas

def colorDistance(pix, targetColor):
    redDifference = pix[0] - targetColor[0]
    greenDifference = pix[1] - targetColor[1]
    blueDifference = pix[2] - targetColor[2]
    distance = (redDifference**2 + greenDifference**2 + blueDifference**2)**0.5
    return distance

def colorChange(img):
    edit_img = img.copy()
    width, height = img.size
    green = (0, 255, 0)
    for x in range(width):
        for y in range(height):
            pix = img.getpixel((x,y))
            if colorDistance(pix, green) < 200:
                edit_img.putpixel((x,y), (0, pix[1], pix[1]))
    return edit_img

def increaseContrast(img):
    edit_img = img.copy()
    width, height = img.size
    for x in range(width-1):
        for y in range(height-1):
            pix = img.getpixel((x,y))
            pix2 = img.getpixel((x+1, y))
            pix3 = img.getpixel((x, y+1))
            if colorDistance(pix, pix2) < 100 or colorDistance(pix, pix3) < 100:
                if pix[0] >= pix[1] and pix[0] >= pix[2]:
                    edit_img.putpixel((x,y), (int(pix[0]*1.3), int(pix[1]), int(pix[2])))
                elif pix[1] >= pix[0] and pix[1] >= pix[2]:
                    edit_img.putpixel((x,y), (int(pix[0]), int(pix[1]*1.3), int(pix[2])))
                else:
                    edit_img.putpixel((x,y), (int(pix[0]), int(pix[1]), int(pix[2]*1.3)))
    return edit_img

def Patterns(img):
    edit_img = img.copy()
    width, height = img.size
    edit_img = colorChange(increaseContrast((edit_img)))
    red = (255, 0, 0)
    blue = (0, 0, 255)
    for x in range(width):
        for y in range(height):
            pix = edit_img.getpixel((x,y))
            if colorDistance(pix, red) < 180 and y % 16 < 8:
                edit_img.putpixel((x,y), (225, pix[1]//3, pix[2]//2))
            if colorDistance(pix, blue) < 215 and y % 24 < 8 and x % 24 < 8:
                edit_img.putpixel((x,y), (pix[0]//2, pix[1]//2, pix[2]))
    return edit_img

def imgOnCanvas(img):
    original_canvas = makeCanvas(img)
    width, height = img.size

    # pastes original image on left 1/3 of canvas with text
    original_canvas.paste(img, (0,0))
    text_original = ImageDraw.Draw(original_canvas)
    font = ImageFont.load_default(60)
    text_original.text((width//2.7, height), "Original Colors", font=font, fill=(0, 0, 0))

    # pasts color changed image on middle 1/3 of canvas with text
    original_canvas.paste(colorChange(increaseContrast(img)), (width+3,0))
    text_color = ImageDraw.Draw(original_canvas)
    text_color.text((width*1.25, height), "Colorblind-friendly Colors", font=font, fill=(0, 0, 0))

    # pastes patterned image on right 1/3 of canvas with text
    original_canvas.paste(Patterns(img), (2*width+6,0))
    text_pattern = ImageDraw.Draw(original_canvas)
    text_pattern.text((width*2.25, height), "Colorblind-friendly Patterns", font=font, fill=(0, 0, 0))

    for i in range(1,3):
        for y in range(height+100):
            original_canvas.putpixel((i*width+1, y), (0, 0, 0))
            original_canvas.putpixel((i*width+2, y), (0, 0, 0))
    return original_canvas

def openImg(files):
    for img in files:
        im = Image.open(img)
        imgOnCanvas(im).show()


files = ["piechart.jpg", "barchart.jpg", "boxplots.jpg", "linechart.jpg"]

openImg(files)
# 4 images will pop up separately one after another.
# Please allow some lag between each image's appearance.