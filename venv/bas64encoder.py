from PIL import Image
import base64

bigimage = Image.open(r'C:\Users\sudeep\Pictures\refresh.png')
smallimage = bigimage.resize((48, 48), Image.ANTIALIAS)
smallimage.save(r'C:\Users\sudeep\Pictures\small_refresh.png', optimize=True)
smallimage.close()
bigimage.close()

f = open(r'C:\Users\sudeep\Pictures\small_refresh.png', 'rb')
pic = f.read()
f.close()
encoded_pic = base64.b64encode(pic)

f = open(r'C:\Users\sudeep\Pictures\refresh.b64.txt', 'wb')
f.write(encoded_pic)
f.close()
