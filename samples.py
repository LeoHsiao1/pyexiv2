import os
from core.use_dll import image


i = image(os.path.abspath(r"core\tests\1.jpg"))
i.read_all()
i.exif_dict
i.iptc_dict
i.xmp_dict

# write the keys you want to change
dict1 = {"Xmp.xmp.Rating": "",  # delete the key if the value is empty
         "Xmp.xmp.CreateDate": "2019-06-23T19:45:17.834"}
# Call this function
i.modify_xmp(dict1)
# read it again
i.read_all()
i.xmp_dict["Xmp.xmp.Rating"]
i.xmp_dict["Xmp.xmp.CreateDate"]
