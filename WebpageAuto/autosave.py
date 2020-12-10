import urllib.request
from selenium import webdriver
url='http://image.baidu.com'
path='/usr/local/chromedriver'

browser = webdriver.Chrome(executable_path=path)

browser.get(url)

kw = browser.find_element_by_id('kw')
if kw:
    kw.send_keys("美女\n")


imgbox = browser.find_element_by_class_name('imgbox')
img = imgbox.find_element_by_tag_name('img')
imgsrc = img.get_attribute('src')

imgf = urllib.request.urlopen(imgsrc)
with open('/tmp/a.jpg', 'wb') as f:
    f.write(imgf.read())
