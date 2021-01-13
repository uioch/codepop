from time import sleep
from PIL import ImageGrab

ims = []
for i in range(20):
    sleep(0.1)
    im=ImageGrab.grab()
    im.save('/tmp/g_' + str(i) + '.png')
    ims.append(im)

im.save('/tmp/g.gif', save_all=True, append_images=ims, loop=1,duration=1)

