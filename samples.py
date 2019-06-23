from core.use_dll import read_exif


# read the metadata
d = read_exif(r"C:\Users\Leo\Desktop\1.jpg")
for k, v in d.items():
    print(k,v)

# modify the dict

# .write(dict)

d = read_exif(r"C:\Users\Leo\Desktop\1副本.jpg")