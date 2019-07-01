import os
from core import image


i = image(os.path.abspath("core/tests/1.jpg"))  # input an image path
i.read_all()    # read all the metadata(including EXIF, IPTC, XMP)
i.exif_dict
i.iptc_dict
i.xmp_dict


dict1={
'Xmp.dc.title': 'lang="x-default" 标题',
'Xmp.MicrosoftPhoto.LastKeywordXMP': '标记1, 标记2',
'Xmp.MicrosoftPhoto.Rating': '75',
'Xmp.dc.creator': '作者', # ?
'Xmp.dc.rights': 'lang="x-default" 版权',
'Xmp.MicrosoftPhoto.DateAcquired': '2019-06-23T19:45:24.297'
}
i.modify_xmp(dict1)
i.read_all()
for k in dict1.keys():
    print(k, '\t', i.xmp_dict[k])
