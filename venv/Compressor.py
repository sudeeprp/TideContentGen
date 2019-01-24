from PIL import Image
import os

def compress(path, filename, max_x, max_y, min_file_bytes):
    filepath = os.path.join(path, filename)
    file_bytes = os.path.getsize(filepath)
    if file_bytes < min_file_bytes:
        return

    bigimage = Image.open(os.path.join(path, filename))
    x, y = bigimage.size
    ratio = x_ratio = y_ratio = 1
    if x > max_x:
        x_ratio = max_x / x
    if y > max_y:
        y_ratio = max_y / y
    ratio = min(x_ratio, y_ratio)
    if ratio != 1:
        x = int(x * ratio)
        y = int(y * ratio)
        smallimage = bigimage.resize((x, y), Image.ANTIALIAS)
    else:
        smallimage = bigimage
    smallimage.save(os.path.join(path, filename), optimize=True)
    smallimage.close()
    bigimage.close()

    compressed_bytes = os.path.getsize(filepath)
    print(filepath + " compressed from " +
          str(file_bytes // 1024) + "KB to " + str(compressed_bytes // 1024) + "KB")

def compress_path(start_dirname, max_x=750, max_y=750, min_file_bytes=500000):
    Image.MAX_IMAGE_PIXELS = None
    for dirName, subdirList, fileList in os.walk(start_dirname):
        for fname in fileList:
            if not fname.startswith('.') and (fname.endswith('png') or fname.endswith('PNG')):
                compress(dirName, fname, max_x, max_y, min_file_bytes)

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 5:
        compress_path(start_dirname=sys.argv[1], max_x=int(sys.argv[2]), max_y=int(sys.argv[3]), min_file_bytes=int(sys.argv[4]))
    else:
        print("Usage: " + sys.argv[0] + " <start dir> <max_x> <max_y> <min_bytes>")
