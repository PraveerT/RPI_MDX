#!/usr/bin/python
import spidev as SPI
import paho.mqtt.client as mqtt
# where the display connects

import time, datetime, sys, signal, urllib, requests, random
from PIL import Image, ImageDraw, ImageFont  # PIL - PythonImageLibrary
from StringIO import StringIO

from EPD_driver import EPD_driver

#time.sleep(30)

mydata=0
#--------------------------------------------------------------------------
##def on_connect(client, userdata, flags, rc):
##    client.subscribe("iotdevice/connectionA")
##
##
##def on_message(client, userdata, msg):
##     mydata=(msg.payload).decode('utf-8')
##     print mydata



#---------------------------------------------------------------------

def handler(signum, frame):
    print ('SIGTERM')
    sys.exit(0)
signal.signal(signal.SIGTERM, handler)
random.seed(time.time())

bus = 0
device = 0
disp = EPD_driver(spi = SPI.SpiDev(bus, device))
print "disp size : %dx%d"%(disp.xDot, disp.yDot)

print '------------init and Clear full screen------------'
disp.Dis_Clear_full()
disp.delay()

# display part
disp.EPD_init_Part()
disp.delay()

imagenames = [] # array of tuples ('http://imagelink','description')

searchnames = ['Cat', 'Horst', 'Amiga', 'DAC', 'Raspberry', 'diy', 'Acorn', 'Boing']

### this writes a bunch of image links ad test descriptions to imagenames
##def querySearchEngine(val):
##    search = "http://api.duckduckgo.com/?q="+val+"&format=json&pretty=1"
##    req = requests.get(search)
##    if req.status_code == 200:
##        del imagenames[:]
##        for topic in req.json()["RelatedTopics"]:
##            if "Topics" in topic:
##                for topic2 in topic["Topics"]:
##                    try:
##                        url = topic2["Icon"]["URL"]
##                        text = topic2["Text"]
##                        if url:
##                            imagenames.append( (url,text) )
##                    except:
##                        # print topic
##                        pass
##            try:
##                url = topic["Icon"]["URL"]
##                text = topic["Text"]
##                if url:
##                    imagenames.append( (url,text) )
##            except:
##                # print topic
##                pass
##    else:
##        print req.status_code
##    print 'search for', val, ' #entries', len(imagenames) #, imagenames
##
### function to write the image to the display
def imageToDisplay(img):
    # prepare for display
    im = mainimg.transpose(Image.ROTATE_90)
    listim = list(im.getdata())
    # print im.format, im.size, im.mode, len(listim)
    # convert to list / bitmap
    listim2 = []
    for y in range(0, im.size[1]):
        for x in range(0, im.size[0]/8):
            val = 0
            for x8 in range(0, 8):
                if listim[(im.size[1]-y-1)*im.size[0] + x*8 + (7-x8)] > 128:
                    # print x,y,x8,'ON'
                    val = val | 0x01 << x8
                else:
                    # print x,y,x8,'OFF'
                    pass
            # print val
            listim2.append(val)
    for x in range(0,1000):
        listim2.append(0)
    # print len(listim2)
    ypos = 0
    xpos = 0
    disp.EPD_Dis_Part(xpos, xpos+im.size[0]-1, ypos, ypos+im.size[1]-1, listim2) # xStart, xEnd, yStart, yEnd, DisBuffer
    uploadtime = time.time()

# font for drawing within PIL
myfont20= ImageFont.truetype("/usr/lib/python2.7/iotfiles/amiga_forever/amiga4ever.ttf", 20)
myfont28 = ImageFont.truetype("/usr/lib/python2.7/iotfiles/amiga_forever/amiga4ever.ttf", 28)

# mainimg is used as screen buffer, all image composing/drawing is done in PIL,
# the mainimg is then copied to the display (drawing on the disp itself is no fun)
mainimg = Image.new("1", (296,128))
draw = ImageDraw.Draw(mainimg)

skip = 0 # used to slow down image changes, but not clock changes
while 1:
    starttime = time.time()
##    if skip == 0:
##        querySearchEngine(searchnames[random.randint(0,len(searchnames)-1)])
##        imagename = imagenames[random.randint(0,len(imagenames)-1)]
        # print '---------------------'
##        try:
##            req = requests.get(imagename[0], stream=True)
##            req.raw.decode_content = True
##            im = Image.open(StringIO(req.content))
##            # print name, im.format, im.size, im.mode
##            im.thumbnail((296,128))
##            im = im.convert("1") #, dither=Image.NONE)
##            # print 'thumbnail', im.format, im.size, im.mode
##            loadtime = time.time()
##            # print 't:load+resize:', (loadtime - starttime)
##
##            # clear
##            draw.rectangle([0,0,296,128], fill=255)
##
##            # copy to mainimg
##            ypos = (disp.xDot - im.size[1])/2
##            xpos = (disp.yDot - im.size[0])/2
##            # print 'ypos:', ypos, 'xpos:', xpos
##            mainimg.paste(im, (xpos,ypos))
##
##            # draw info text
##            ts = draw.textsize(imagename[1], font=myfont10)
##            tsy = ts[1]+1
##            oldy = -1
##            divs = ts[0]/250
##            for y in range(0, divs):
##                newtext = imagename[1][(oldy+1)*len(imagename[1])/divs:(y+1)*len(imagename[1])/divs]
##                # print divs, oldy, y, newtext
##                oldy = y
##                draw.text((1, 1+y*tsy), newtext, fill=255, font=myfont10)
##                draw.text((1, 3+y*tsy), newtext, fill=255, font=myfont10)
##                draw.text((3, 3+y*tsy), newtext, fill=255, font=myfont10)
##                draw.text((3, 1+y*tsy), newtext, fill=255, font=myfont10)
##                draw.text((2, 2+y*tsy), newtext, fill=0, font=myfont10)
##
##        except IOError as ex:
##            print 'IOError', str(ex), imagename[0]
##            pass

#--------------------------------------------data

##
##    client = mqtt.Client()
##    client.on_connect = on_connect
##    client.on_message = on_message
##
##
##    client.connect("test.mosquitto.org", 1883, 60)
##    client.loop(10)
##

#--------------------------------------------data

    tpx = 0
    tpy = 5
    file = open("/usr/lib/python2.7/iotfiles/testfile.txt", "r")

    mydata= file.read()
    Temp=str(mydata)[:5]
    print mydata

###-----------------------------------------------temp string    
##    
##
##
##
##
##
      
##
##    draw.text((tpx-1, tpy ), "temp", fill=255, font=myfont10)
##    draw.text((tpx-1, tpy-1), "temp", fill=255, font=myfont10)
##    draw.text((tpx  , tpy-1), "temp", fill=255, font=myfont10)
##    draw.text((tpx1+2, tpy ), "temp", fill=255, font=myfont10)
##    draw.text((tpx1  , tpy1  ), "temp", fill=0, font=myfont10)
##
##        
##
##
###-----------------------------------------------temp string
##       
    tpx1 = 0
    tpy1 = 5
    
##    for i in range(tpy-4, tpy+32, 2):
##
##
##
##
##
##       draw.line([0, i, 295, i], fill=255)
##
##       draw.text((tpx1-1, tpy1 ), "Temp:", fill=0, font=myfont20)
##       draw.text((tpx1-1, tpy1-1), "Temp:", fill=0, font=myfont20)
##       draw.text((tpx1  , tpy1-1), "Temp:", fill=0, font=myfont20)
##       draw.text((tpx1+2, tpy1 ), "Temp:", fill=0, font=myfont20)
##       draw.text((tpx1+2, tpy1+2), "Temp:", fill=0, font=myfont20)
##       draw.text((tpx1  , tpy1+2), "Temp:", fill=0, font=myfont20)
##       draw.text((tpx1  , tpy1  ), "Temp:", fill=255, font=myfont20)
##
##
##    tpx1 = 75
##    tpy1 = 5
##    
##    for i in range(tpy-4, tpy+32, 2):
##
##
##
##
##
##       draw.line([0, i, 295, i], fill=255)
##
##       draw.text((tpx1-1, tpy1 ), Temp, fill=0, font=myfont20)
##       draw.text((tpx1-1, tpy1-1), Temp, fill=0, font=myfont20)
##       draw.text((tpx1  , tpy1-1), Temp, fill=0, font=myfont20)
##       draw.text((tpx1+2, tpy1 ), Temp, fill=0, font=myfont20)
##       draw.text((tpx1+2, tpy1+2), Temp, fill=0, font=myfont20)
##       draw.text((tpx1  , tpy1+2), Temp, fill=0, font=myfont20)
##       draw.text((tpx1  , tpy1  ), Temp, fill=255, font=myfont20)  



#-----------------------------------------------humidity

    tpx1 = 0
##    tpy1 = 45
##    draw.line([0,, 295, 1], fill=0)

    for i in range(0, 130, 1):

         



        draw.line([0, i, 295, i], fill=255)


        draw.text((0, 0), "TEMP:", font=myfont20)
        draw.text((0, 25), "CO2:", font=myfont20)
        draw.text((0, 50), "HUM:", font=myfont20)
        draw.text((0, 75), "O3:", font=myfont20)
        draw.text((100, 0), mydata[:5], font=myfont20)
        draw.text((80, 25), mydata[5:10], font=myfont20)
        draw.text((0, 0), "TEMP:", font=myfont20) 
    ##       draw.text((tpx1-1, tpy1 ), "Hum:", fill=0, font=myfont20)
##       draw.text((tpx1-1, tpy1-1), "Hum:", fill=0, font=myfont20)
##       draw.text((tpx1  , tpy-1), "Hum:", fill=0, font=myfont20)
##       draw.text((tpx1+2, tpy1 ), "Hum:", fill=0, font=myfont20)
##       draw.text((tpx1+2, tpy1+2), "Hum:", fill=0, font=myfont20)
##       draw.text((tpx1  , tpy1+2), "Hum:", fill=0, font=myfont20)
##       draw.text((tpx1  , tpy1  ), "Hum:", fill=255, font=myfont20)
       
       

    # print 't:draw:', (drawtime - loadtime)

    convtime = time.time()
    # print 't:conv:', (convtime - loadtime)

    # disp.delay()

    imageToDisplay(mainimg)
    skip = (skip+1)%17

    # print 't:upload:', (uploadtime - loadtime)


