import pyexiv2

img = pyexiv2.Image(r'./pyexiv2/tests/data/1.jpg')
img.read_exif()
img.modify_exif({'Exif.Image.Make': 'test-中文-', 'Exif.Image.Rating': ''})
img.close()
