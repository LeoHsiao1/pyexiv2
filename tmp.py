from pyexiv2 import Image

img = Image(r'd:\1\pyexiv2\pyexiv2\tests\1.jpg')
# img = Image('./pyexiv2/tests/1.jpg')
img.read_exif()
img.read_iptc()
img.read_xmp()
img.read_raw_xmp()

img.modify_exif({'Exif.Image.Make': 'test-中文-', 'Exif.Image.Rating': ''})
img.read_exif()

img.clear_exif()
img.read_exif()

dict1 = {"Xmp.xmp.CreateDate": "2019-06-23T19:45:17.834",
            "Xmp.xmp.Rating": "",
            "Xmp.dc.subject": ["flag1中文", "flag2中文", "flag3中文"]}
img.modify_xmp(dict1)

# from pyexiv2.lib import api
# dir(api)
