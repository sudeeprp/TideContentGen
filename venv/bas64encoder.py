from PIL import Image
import base64

bigimage = Image.open(r'C:\Users\sudeep\Pictures\guest.png')
smallimage = bigimage.resize((100, 100), Image.ANTIALIAS)
smallimage.save(r'C:\Users\sudeep\Pictures\small_guest.png', optimize=True)
smallimage.close()
bigimage.close()

f = open(r'C:\Users\sudeep\Pictures\small_guest.png', 'rb')
pic = f.read()
f.close()
encoded_pic = base64.b64encode(pic)

f = open(r'C:\Users\sudeep\Pictures\guest.b64.txt', 'wb')
f.write(encoded_pic)
f.close()
