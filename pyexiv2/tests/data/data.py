import os


current_dir = os.path.dirname(__file__)

with open(os.path.join(current_dir, 'gray.icc'), 'rb') as f:
    GRAY_ICC = f.read()

with open(os.path.join(current_dir, 'rgb.icc'), 'rb') as f:
    RGB_ICC = f.read()

with open(os.path.join(current_dir, '1-thumb.jpg'), 'rb') as f:
    EXIF_THUMB = f.read()

PIXEL_WIDTH  = 200
PIXEL_HEIGHT = 200
MIME_TYPE   = 'image/jpeg'

ACCESS_MODE = {
    'exif'   : 'read+write',
    'iptc'   : 'read+write',
    'xmp'    : 'read+write',
    'comment': 'read+write',
}

COMMENT = 'Hello World!  \n你好！\n'

EXIF_DETAIL = {
    'Exif.Image.ImageDescription': {
        'idx': 1,
        'ifdName': 'IFD0',
        'tagDesc': 'A character string giving the title of the image. It may be a comment such as "1988 company picnic" or the like. Two-bytes character codes cannot be used. When a 2-bytes code is necessary, the Exif Private tag <UserComment> is to be used.',
        'tagLabel': 'Image Description',
        'tagNumber': 270,
        'typeName': 'Ascii',
        'value': 'test-中文-'
    },
    'Exif.Image.Make': {
        'idx': 2,
        'ifdName': 'IFD0',
        'tagDesc': 'The manufacturer of the recording equipment. This is the manufacturer of the DSC, scanner, video digitizer or other equipment that generated the image. When the field is left blank, it is treated as unknown.',
        'tagLabel': 'Manufacturer',
        'tagNumber': 271,
        'typeName': 'Ascii',
        'value': 'test-中文-'
    },
    'Exif.Image.Model': {
        'idx': 3,
        'ifdName': 'IFD0',
        'tagDesc': 'The model name or model number of the equipment. This is the model name or number of the DSC, scanner, video digitizer or other equipment that generated the image. When the field is left blank, it is treated as unknown.',
        'tagLabel': 'Model',
        'tagNumber': 272,
        'typeName': 'Ascii',
        'value': 'test-中文-'
    },
    'Exif.Image.Orientation': {
        'idx': 4,
        'ifdName': 'IFD0',
        'tagDesc': 'The image orientation viewed in terms of rows and columns.',
        'tagLabel': 'Orientation',
        'tagNumber': 274,
        'typeName': 'Ascii',
        'value': ['1',
                  '2',
                  '3']
    },
    'Exif.Image.DateTime': {
        'idx': 7,
        'ifdName': 'IFD0',
        'tagDesc': 'The date and time of image creation. In Exif standard, it is the date and time the file was changed.',
        'tagLabel': 'Date and Time',
        'tagNumber': 306,
        'typeName': 'Ascii',
        'value': '2019:08:12 19:44:04'
    },
    'Exif.Image.Artist': {
        'idx': 8,
        'ifdName': 'IFD0',
        'tagDesc': 'This tag records the name of the camera owner, photographer or image creator. The detailed format is not specified, but it is recommended that the information be written as in the example below for ease of Interoperability. When the field is left blank, it is treated as unknown. Ex.) "Camera owner, John Smith; Photographer, Michael Brown; Image creator, Ken James"',
        'tagLabel': 'Artist',
        'tagNumber': 315,
        'typeName': 'Ascii',
        'value': 'test-中文-'
    },
    'Exif.Image.Rating': {
        'idx': 9,
        'ifdName': 'IFD0',
        'tagDesc': 'Rating tag used by Windows',
        'tagLabel': 'Windows Rating',
        'tagNumber': 18246,
        'typeName': 'Short',
        'value': '4'
    },
    'Exif.Image.RatingPercent': {
        'idx': 10,
        'ifdName': 'IFD0',
        'tagDesc': 'Rating tag used by Windows, value in percent',
        'tagLabel': 'Windows Rating Percent',
        'tagNumber': 18249,
        'typeName': 'Short',
        'value': '75'
    },
    'Exif.Image.Copyright': {
        'idx': 11,
        'ifdName': 'IFD0',
        'tagDesc': 'Copyright information. In this standard the tag is used to indicate both the photographer and editor copyrights. It is the copyright notice of the person or organization claiming rights to the image. The Interoperability copyright statement including date and rights should be written in this field; e.g., "Copyright, John Smith, 19xx. All rights reserved.". In this standard the field records both the photographer and editor copyrights, with each recorded in a separate part of the statement. When there is a clear distinction between the photographer and editor copyrights, these are to be written in the order of photographer followed by editor copyright, separated by NULL (in this case since the statement also ends with a NULL, there are two NULL codes). When only the photographer copyright is given, it is terminated by one NULL code. When only the editor copyright is given, the photographer copyright part consists of one space followed by a terminating NULL code, then the editor copyright is given. When the field is left blank, it is treated as unknown.',
        'tagLabel': 'Copyright',
        'tagNumber': 33432,
        'typeName': 'Ascii',
        'value': 'test-中文-'
    },
    'Exif.Image.ExifTag': {
        'idx': 12,
        'ifdName': 'IFD0',
        'tagDesc': 'A pointer to the Exif IFD. Interoperability, Exif IFD has the same structure as that of the IFD specified in TIFF. ordinarily, however, it does not contain image data as in the case of TIFF.',
        'tagLabel': 'Exif IFD Pointer',
        'tagNumber': 34665,
        'typeName': 'Long',
        'value': '2470'
    },
    'Exif.Photo.ExposureProgram': {
        'idx': 1,
        'ifdName': 'Exif',
        'tagDesc': 'The class of the program used by the camera to set exposure when the picture is taken.',
        'tagLabel': 'Exposure Program',
        'tagNumber': 34850,
        'typeName': 'Short',
        'value': '1'
    },
    'Exif.Photo.ExifVersion': {
        'idx': 2,
        'ifdName': 'Exif',
        'tagDesc': 'The version of this standard supported. Nonexistence of this field is taken to mean nonconformance to the standard.',
        'tagLabel': 'Exif Version',
        'tagNumber': 36864,
        'typeName': 'Undefined',
        'value': '48 50 50 49'
    },
    'Exif.Photo.DateTimeOriginal': {
        'idx': 3,
        'ifdName': 'Exif',
        'tagDesc': 'The date and time when the original image data was generated. For a digital still camera the date and time the picture was taken are recorded.',
        'tagLabel': 'Date and Time (original)',
        'tagNumber': 36867,
        'typeName': 'Ascii',
        'value': '2019:08:12 19:44:04'
    },
    'Exif.Photo.DateTimeDigitized': {
        'idx': 4,
        'ifdName': 'Exif',
        'tagDesc': 'The date and time when the image was stored as digital data.',
        'tagLabel': 'Date and Time (digitized)',
        'tagNumber': 36868,
        'typeName': 'Ascii',
        'value': '2019:08:12 19:44:04'
    },
    'Exif.Photo.LightSource': {
        'idx': 5,
        'ifdName': 'Exif',
        'tagDesc': 'The kind of light source.',
        'tagLabel': 'Light Source',
        'tagNumber': 37384,
        'typeName': 'Short',
        'value': '1'
    },
    'Exif.Photo.SubSecTime': {
        'idx': 6,
        'ifdName': 'Exif',
        'tagDesc': 'A tag used to record fractions of seconds for the <DateTime> tag.',
        'tagLabel': 'Sub-seconds Time',
        'tagNumber': 37520,
        'typeName': 'Ascii',
        'value': '18'
    },
    'Exif.Photo.SubSecTimeOriginal': {
        'idx': 7,
        'ifdName': 'Exif',
        'tagDesc': 'A tag used to record fractions of seconds for the <DateTimeOriginal> tag.',
        'tagLabel': 'Sub-seconds Time Original',
        'tagNumber': 37521,
        'typeName': 'Ascii',
        'value': '18'
    },
    'Exif.Photo.SubSecTimeDigitized': {
        'idx': 8,
        'ifdName': 'Exif',
        'tagDesc': 'A tag used to record fractions of seconds for the <DateTimeDigitized> tag.',
        'tagLabel': 'Sub-seconds Time Digitized',
        'tagNumber': 37522,
        'typeName': 'Ascii',
        'value': '176'
    },
    'Exif.Photo.ColorSpace': {
        'idx': 9,
        'ifdName': 'Exif',
        'tagDesc': 'The color space information tag is always recorded as the color space specifier. Normally sRGB is used to define the color space based on the PC monitor conditions and environment. If a color space other than sRGB is used, Uncalibrated is set. Image data recorded as Uncalibrated can be treated as sRGB when it is converted to FlashPix.',
        'tagLabel': 'Color Space',
        'tagNumber': 40961,
        'typeName': 'Short',
        'value': '65535'
    },
    'Exif.Photo.WhiteBalance': {
        'idx': 10,
        'ifdName': 'Exif',
        'tagDesc': 'This tag indicates the white balance mode set when the image was shot.',
        'tagLabel': 'White Balance',
        'tagNumber': 41987,
        'typeName': 'Short',
        'value': '0'
    },
    'Exif.Photo.Contrast': {
        'idx': 11,
        'ifdName': 'Exif',
        'tagDesc': 'This tag indicates the direction of contrast processing applied by the camera when the image was shot.',
        'tagLabel': 'Contrast',
        'tagNumber': 41992,
        'typeName': 'Short',
        'value': '0'
    },
    'Exif.Photo.Saturation': {
        'idx': 12,
        'ifdName': 'Exif',
        'tagDesc': 'This tag indicates the direction of saturation processing applied by the camera when the image was shot.',
        'tagLabel': 'Saturation',
        'tagNumber': 41993,
        'typeName': 'Short',
        'value': '0'
    },
    'Exif.Photo.Sharpness': {
        'idx': 13,
        'ifdName': 'Exif',
        'tagDesc': 'This tag indicates the direction of sharpness processing applied by the camera when the image was shot.',
        'tagLabel': 'Sharpness',
        'tagNumber': 41994,
        'typeName': 'Short',
        'value': '0'
    },
    'Exif.Photo.0xea1c': {
        'idx': 14,
        'ifdName': 'Exif',
        'tagDesc': '',
        'tagLabel': '',
        'tagNumber': 59932,
        'typeName': 'Undefined',
        'value': '28 234 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'
    },
    'Exif.Image.XPTitle': {
        'idx': 13,
        'ifdName': 'IFD0',
        'tagDesc': 'Title tag used by Windows, encoded in UCS2',
        'tagLabel': 'Windows Title',
        'tagNumber': 40091,
        'typeName': 'Byte',
        'value': 'test-中文-\x00'
    },
    'Exif.Image.XPComment': {
        'idx': 14,
        'ifdName': 'IFD0',
        'tagDesc': 'Comment tag used by Windows, encoded in UCS2',
        'tagLabel': 'Windows Comment',
        'tagNumber': 40092,
        'typeName': 'Byte',
        'value': 'test-中文-\x00'
    },
    'Exif.Image.XPAuthor': {
        'idx': 15,
        'ifdName': 'IFD0',
        'tagDesc': 'Author tag used by Windows, encoded in UCS2',
        'tagLabel': 'Windows Author',
        'tagNumber': 40093,
        'typeName': 'Byte',
        'value': 'test-中文-\x00'
    },
    'Exif.Image.XPKeywords': {
        'idx': 16,
        'ifdName': 'IFD0',
        'tagDesc': 'Keywords tag used by Windows, encoded in UCS2',
        'tagLabel': 'Windows Keywords',
        'tagNumber': 40094,
        'typeName': 'Byte',
        'value': 'test-中文-\x00'
    },
    'Exif.Image.XPSubject': {
        'idx': 17,
        'ifdName': 'IFD0',
        'tagDesc': 'Subject tag used by Windows, encoded in UCS2',
        'tagLabel': 'Windows Subject',
        'tagNumber': 40095,
        'typeName': 'Byte',
        'value': 'test-中文-\x00'
    },
    'Exif.Image.0xea1c': {
        'idx': 18,
        'ifdName': 'IFD0',
        'tagDesc': '',
        'tagLabel': '',
        'tagNumber': 59932,
        'typeName': 'Undefined',
        'value': '28 234 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'
    },
    'Exif.Thumbnail.Compression': {
        'idx': 1,
        'ifdName': 'IFD1',
        'tagDesc': 'The compression scheme used for the image data. When a primary image is JPEG compressed, this designation is not necessary and is omitted. When thumbnails use JPEG compression, this tag value is set to 6.',
        'tagLabel': 'Compression',
        'tagNumber': 259,
        'typeName': 'Short',
        'value': '6'
    },
    'Exif.Thumbnail.JPEGInterchangeFormat': {
        'idx': 2,
        'ifdName': 'IFD1',
        'tagDesc': 'The offset to the start byte (SOI) of JPEG compressed thumbnail data. This is not used for primary image JPEG data.',
        'tagLabel': 'JPEG Interchange Format',
        'tagNumber': 513,
        'typeName': 'Long',
        'value': '4786'
    },
    'Exif.Thumbnail.JPEGInterchangeFormatLength': {
        'idx': 3,
        'ifdName': 'IFD1',
        'tagDesc': 'The number of bytes of JPEG compressed thumbnail data. This is not used for primary image JPEG data. JPEG thumbnails are not divided but are recorded as a continuous JPEG bitstream from SOI to EOI. Appn and COM markers should not be recorded. Compressed thumbnails must be recorded in no more than 64 Kbytes, including all other data to be recorded in APP1.',
        'tagLabel': 'JPEG Interchange Format Length',
        'tagNumber': 514,
        'typeName': 'Long',
        'value': '6969'
    }
}

EXIF = {tag:tag_detail['value'] for tag,tag_detail in EXIF_DETAIL.items()}

IPTC_DETAIL = {
    'Iptc.Envelope.CharacterSet': {
        'tagDesc': 'This tag consisting of one or more control functions used for the announcement, invocation or designation of coded character sets. The control functions follow the ISO 2022 standard and may consist of the escape control character and one or more graphic characters.',
        'tagLabel': 'Character Set',
        'tagNumber': 90,
        'typeName': 'String',
        'value': '\x1b%G'
    },
    'Iptc.Application2.RecordVersion': {
        'tagDesc': 'A binary number identifying the version of the Information Interchange Model, Part II, utilised by the provider. Version numbers are assigned by IPTC and NAA organizations.',
        'tagLabel': 'Record Version',
        'tagNumber': 0,
        'typeName': 'Short',
        'value': '4'
    },
    'Iptc.Application2.ObjectName': {
        'tagDesc': 'Used as a shorthand reference for the object. Changes to exist-ing data, such as updated stories or new crops on photos, should be identified in tag <EditStatus>.',
        'tagLabel': 'Object Name',
        'tagNumber': 5,
        'typeName': 'String',
        'value': 'test-中文-'
    },
    'Iptc.Application2.Keywords': {
        'tagDesc': 'Used to indicate specific information retrieval words. It is expected that a provider of various types of data that are related in subject matter uses the same keyword, enabling the receiving system or subsystems to search across all types of data for related material.',
        'tagLabel': 'Keywords',
        'tagNumber': 25,
        'typeName': 'String',
        'value': ['tag1',
                  'tag2',
                  'tag3']
    },
    'Iptc.Application2.DateCreated': {
        'tagDesc': 'Represented in the form CCYYMMDD to designate the date the intellectual content of the object data was created rather than the date of the creation of the physical representation. Follows ISO 8601 standard.',
        'tagLabel': 'Date Created',
        'tagNumber': 55,
        'typeName': 'Date',
        'value': '2019-08-12'
    },
    'Iptc.Application2.TimeCreated': {
        'tagDesc': 'Represented in the form HHMMSS:HHMM to designate the time the intellectual content of the object data current source material was created rather than the creation of the physical representation. Follows ISO 8601 standard.',
        'tagLabel': 'Time Created',
        'tagNumber': 60,
        'typeName': 'Time',
        'value': '19:44:04+00:00'
    },
    'Iptc.Application2.Byline': {
        'tagDesc': 'Contains name of the creator of the object data, e.g. writer, photographer or graphic artist.',
        'tagLabel': 'By-line',
        'tagNumber': 80,
        'typeName': 'String',
        'value': ['test-中文-']
    },
    'Iptc.Application2.Copyright': {
        'tagDesc': 'Contains any necessary copyright notice.',
        'tagLabel': 'Copyright',
        'tagNumber': 116,
        'typeName': 'String',
        'value': 'test-中文-'
    },
    'Iptc.Application2.Caption': {
        'tagDesc': 'A textual description of the object data.',
        'tagLabel': 'Caption',
        'tagNumber': 120,
        'typeName': 'String',
        'value': 'test-中文-'
    }
}

IPTC = {tag:tag_detail['value'] for tag,tag_detail in IPTC_DETAIL.items()}

XMP_DETAIL = {
    'Xmp.dc.format': {
        'value': 'image/jpeg',
        'typeName': 'XmpText',
        'tagDesc': 'The file format used when saving the resource. Tools and applications should set this property to the save format of the data. It may include appropriate qualifiers.',
        'tagLabel': 'Format'
    },
    'Xmp.dc.subject': {
        'value': ['tag1', 'tag2', 'tag3'],
        'typeName': 'XmpBag',
        'tagDesc': 'An unordered array of descriptive phrases or keywords that specify the topic of the content of the resource.',
        'tagLabel': 'Subject'
    },
    'Xmp.dc.creator': {
        'value': ['test-中文-'],
        'typeName': 'XmpSeq',
        'tagDesc': 'The authors of the resource (listed in order of precedence, if significant).',
        'tagLabel': 'Creator'
    },
    'Xmp.dc.title': {
        'value': {
            'lang="x-default"': 'test-中文-',
            'lang="de-DE"': 'Hallo, Welt'
        },
        'typeName': 'LangAlt',
        'tagDesc': 'The title of the document, or the name given to the resource. Typically, it will be a name by which the resource is formally known.',
        'tagLabel': 'Title'
    },
    'Xmp.dc.rights': {
        'value': {
            'lang="x-default"': 'test-中文-'
        },
        'typeName': 'LangAlt',
        'tagDesc': 'Informal rights statement, selected by language. Typically, rights information includes a statement about various property rights associated with the resource, including intellectual property rights.',
        'tagLabel': 'Rights'
    },
    'Xmp.dc.description': {
        'value': {
            'lang="x-default"': 'test-中文-'
        },
        'typeName': 'LangAlt',
        'tagDesc': 'A textual description of the content of the resource. Multiple values may be present for different languages.',
        'tagLabel': 'Description'
    },
    'Xmp.xmp.Rating': {
        'value': '4',
        'typeName': 'XmpText',
        'tagDesc': "A number that indicates a document's status relative to other documents, used to organize documents in a file browser. Values are user-defined within an application-defined range.",
        'tagLabel': 'Rating'
    },
    'Xmp.xmp.CreateDate': {
        'value': '2019-08-12T19:44:04.176',
        'typeName': 'XmpText',
        'tagDesc': 'The date and time the resource was originally created.',
        'tagLabel': 'Create Date'
    },
    'Xmp.xmp.ModifyDate': {
        'value': '2019-08-12T19:44:04.18',
        'typeName': 'XmpText',
        'tagDesc': "The date and time the resource was last modified. Note: The value of this property is not necessarily the same as the file's system modification date because it is set before the file is saved.",
        'tagLabel': 'Modify Date'
    },
    'Xmp.xmp.MetadataDate': {
        'value': '2020-04-06T00:55:07+08:00',
        'typeName': 'XmpText',
        'tagDesc': 'The date and time that any metadata for this resource was last changed. It should be the same as or more recent than xmp:ModifyDate.',
        'tagLabel': 'Metadata Date'
    },
    'Xmp.MicrosoftPhoto.Rating': {
        'value': '75',
        'typeName': 'XmpText',
        'tagDesc': 'Rating Percent.',
        'tagLabel': 'Rating Percent'
    },
    'Xmp.MicrosoftPhoto.DateAcquired': {
        'value': '2019-08-12T19:44:08.151',
        'typeName': 'XmpText',
        'tagDesc': 'Date Acquired.',
        'tagLabel': 'Date Acquired'
    },
    'Xmp.MicrosoftPhoto.LensModel': {
        'value': 'test-中文-',
        'typeName': 'XmpText',
        'tagDesc': 'Lens Model.',
        'tagLabel': 'Lens Model'
    },
    'Xmp.MicrosoftPhoto.LensManufacturer': {
        'value': 'test-中文-',
        'typeName': 'XmpText',
        'tagDesc': 'Lens Manufacturer.',
        'tagLabel': 'Lens Manufacturer'
    },
    'Xmp.MicrosoftPhoto.FlashModel': {
        'value': 'test-中文-',
        'typeName': 'XmpText',
        'tagDesc': 'Flash Model.',
        'tagLabel': 'Flash Model'
    },
    'Xmp.MicrosoftPhoto.FlashManufacturer': {
        'value': 'test-中文-',
        'typeName': 'XmpText',
        'tagDesc': 'Flash Manufacturer.',
        'tagLabel': 'Flash Manufacturer'
    },
    'Xmp.MicrosoftPhoto.CameraSerialNumber': {
        'value': 'test-中文-',
        'typeName': 'XmpText',
        'tagDesc': 'Camera Serial Number.',
        'tagLabel': 'Camera Serial Number'
    },
    'Xmp.MicrosoftPhoto.LastKeywordXMP': {
        'value': ['test-中文-'],
        'typeName': 'XmpBag',
        'tagDesc': 'Last Keyword XMP.',
        'tagLabel': 'Last Keyword XMP'
    },
    'Xmp.xmpMM.InstanceID': {
        'value': 'xmp.iid:14282d1f-7831-7043-ad77-1e10959ecd50',
        'typeName': 'XmpText',
        'tagDesc': 'An identifier for a specific incarnation of a document, updated each time a file is saved. It should be based on a UUID; see Document and Instance IDs below.',
        'tagLabel': 'Instance ID'
    },
    'Xmp.xmpMM.DocumentID': {
        'value': 'ECE1099AF3406874FAA7B01CBB5C6F71',
        'typeName': 'XmpText',
        'tagDesc': 'The common identifier for all versions and renditions of a document. It should be based on a UUID; see Document and Instance IDs below.',
        'tagLabel': 'Document ID'
    },
    'Xmp.xmpMM.OriginalDocumentID': {
        'value': 'ECE1099AF3406874FAA7B01CBB5C6F71',
        'typeName': 'XmpText',
        'tagDesc': 'Refer to Part 1, Data Model, Serialization, and Core Properties, for definition.',
        'tagLabel': 'Original Document ID'
    },
    'Xmp.xmpMM.History': {
        'value': [''],
        'typeName': 'XmpText',
        'tagDesc': 'An ordered array of high-level user actions that resulted in this resource. It is intended to give human readers a general indication of the steps taken to make the changes from the previous version to this one. The list should be at an abstract level; it is not intended to be an exhaustive keystroke or other detailed history.',
        'tagLabel': 'History'
    },
    'Xmp.xmpMM.History[1]': {
        'value': 'type="Struct"',
        'typeName': 'XmpText',
        'tagDesc': '',
        'tagLabel': 'History[1]'
    },
    'Xmp.xmpMM.History[1]/stEvt:action': {
        'value': 'saved',
        'typeName': 'XmpText',
        'tagDesc': '',
        'tagLabel': 'History[1]/stEvt:action'
    },
    'Xmp.xmpMM.History[1]/stEvt:instanceID': {
        'value': 'xmp.iid:8f83ee32-1163-7b40-b31b-deab20789cf4',
        'typeName': 'XmpText',
        'tagDesc': '',
        'tagLabel': 'History[1]/stEvt:instanceID'
    },
    'Xmp.xmpMM.History[1]/stEvt:when': {
        'value': '2019-08-19T19:45:55+08:00',
        'typeName': 'XmpText',
        'tagDesc': '',
        'tagLabel': 'History[1]/stEvt:when'
    },
    'Xmp.xmpMM.History[1]/stEvt:softwareAgent': {
        'value': 'Adobe Photoshop Camera Raw 10.0',
        'typeName': 'XmpText',
        'tagDesc': '',
        'tagLabel': 'History[1]/stEvt:softwareAgent'
    },
    'Xmp.xmpMM.History[1]/stEvt:changed': {
        'value': '/metadata',
        'typeName': 'XmpText',
        'tagDesc': '',
        'tagLabel': 'History[1]/stEvt:changed'
    },
    'Xmp.xmpMM.History[2]': {
        'value': 'type="Struct"',
        'typeName': 'XmpText',
        'tagDesc': '',
        'tagLabel': 'History[2]'
    },
    'Xmp.xmpMM.History[2]/stEvt:action': {
        'value': 'saved',
        'typeName': 'XmpText',
        'tagDesc': '',
        'tagLabel': 'History[2]/stEvt:action'
    },
    'Xmp.xmpMM.History[2]/stEvt:instanceID': {
        'value': 'xmp.iid:14282d1f-7831-7043-ad77-1e10959ecd50',
        'typeName': 'XmpText',
        'tagDesc': '',
        'tagLabel': 'History[2]/stEvt:instanceID'
    },
    'Xmp.xmpMM.History[2]/stEvt:when': {
        'value': '2020-04-06T00:55:07+08:00',
        'typeName': 'XmpText',
        'tagDesc': '',
        'tagLabel': 'History[2]/stEvt:when'
    },
    'Xmp.xmpMM.History[2]/stEvt:softwareAgent': {
        'value': 'Adobe Photoshop Camera Raw (Windows)',
        'typeName': 'XmpText',
        'tagDesc': '',
        'tagLabel': 'History[2]/stEvt:softwareAgent'
    },
    'Xmp.xmpMM.History[2]/stEvt:changed': {
        'value': '/metadata',
        'typeName': 'XmpText',
        'tagDesc': '',
        'tagLabel': 'History[2]/stEvt:changed'
    },
    'Xmp.photoshop.DateCreated': {
        'value': '2019-08-12T19:44:04Z',
        'typeName': 'XmpText',
        'tagDesc': 'The date the intellectual content of the document was created (rather than the creation date of the physical representation), following IIM conventions. For example, a photo taken during the American Civil War would have a creation date during that epoch (1861-1865) rather than the date the photo was digitized for archiving.',
        'tagLabel': 'Date Created'
    },
    'Xmp.iptc.CreatorContactInfo': {
        'value': 'type="Struct"',
        'typeName': 'XmpText',
        'tagDesc': "The creator's contact information provides all necessary information to get in contact with the creator of this image and comprises a set of sub-properties for proper addressing.",
        'tagLabel': "Creator's Contact Info"
    },
    'Xmp.iptc.CreatorContactInfo/Iptc4xmpCore:CiTelWork': {
        'value': '123456',
        'typeName': 'XmpText',
        'tagDesc': 'Deprecated, use the CiTelWork tag in ContactInfo struct instead. sub-key Creator Contact Info: phone number.',
        'tagLabel': 'Contact Info-Phone (deprecated)'
    },
    'Xmp.iptc.CreatorContactInfo/Iptc4xmpCore:CiEmailWork': {
        'value': '123456@gmail.com',
        'typeName': 'XmpText',
        'tagDesc': 'Deprecated, use the CiEmailWork tag in ContactInfo struct instead. sub-key Creator Contact Info: email address.',
        'tagLabel': 'Contact Info-Email (deprecated)'
    },
    'Xmp.iptc.CreatorContactInfo/Iptc4xmpCore:CiUrlWork': {
        'value': 'www.123456.com',
        'typeName': 'XmpText',
        'tagDesc': 'Deprecated, use the CiUrlWork tag in ContactInfo struct instead. sub-key Creator Contact Info: web address.',
        'tagLabel': 'Contact Info-Web URL (deprecated)'
    }
}

XMP = {tag:tag_detail['value'] for tag,tag_detail in XMP_DETAIL.items()}

RAW_XMP = """
<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?> <x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 4.4.0-Exiv2"> <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"> <rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xmp="http://ns.adobe.com/xap/1.0/" xmlns:MicrosoftPhoto="http://ns.microsoft.com/photo/1.0/" xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/" xmlns:stEvt="http://ns.adobe.com/xap/1.0/sType/ResourceEvent#" xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/" xmlns:Iptc4xmpCore="http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/" dc:format="image/jpeg" xmp:Rating="4" xmp:CreateDate="2019-08-12T19:44:04.176" xmp:ModifyDate="2019-08-12T19:44:04.18" xmp:MetadataDate="2020-04-06T00:55:07+08:00" MicrosoftPhoto:Rating="75" MicrosoftPhoto:DateAcquired="2019-08-12T19:44:08.151" MicrosoftPhoto:LensModel="test-中文-" MicrosoftPhoto:LensManufacturer="test-中文-" MicrosoftPhoto:FlashModel="test-中文-" MicrosoftPhoto:FlashManufacturer="test-中文-" MicrosoftPhoto:CameraSerialNumber="test-中文-" xmpMM:InstanceID="xmp.iid:14282d1f-7831-7043-ad77-1e10959ecd50" xmpMM:DocumentID="ECE1099AF3406874FAA7B01CBB5C6F71" xmpMM:OriginalDocumentID="ECE1099AF3406874FAA7B01CBB5C6F71" photoshop:DateCreated="2019-08-12T19:44:04Z"> <dc:subject> <rdf:Bag> <rdf:li>tag1</rdf:li> <rdf:li>tag2</rdf:li> <rdf:li>tag3</rdf:li> </rdf:Bag> </dc:subject> <dc:creator> <rdf:Seq> <rdf:li>test-中文-</rdf:li> </rdf:Seq> </dc:creator> <dc:title> <rdf:Alt> <rdf:li xml:lang="x-default">test-中文-, lang="de-DE" Hallo, Welt</rdf:li> </rdf:Alt> </dc:title> <dc:rights> <rdf:Alt> <rdf:li xml:lang="x-default">test-中文-</rdf:li> </rdf:Alt> </dc:rights> <dc:description> <rdf:Alt> <rdf:li xml:lang="x-default">test-中文-</rdf:li> </rdf:Alt> </dc:description> <MicrosoftPhoto:LastKeywordXMP> <rdf:Bag> <rdf:li>test-中文-</rdf:li> </rdf:Bag> </MicrosoftPhoto:LastKeywordXMP> <xmpMM:History> <rdf:Seq> <rdf:li stEvt:action="saved" stEvt:instanceID="xmp.iid:8f83ee32-1163-7b40-b31b-deab20789cf4" stEvt:when="2019-08-19T19:45:55+08:00" stEvt:softwareAgent="Adobe Photoshop Camera Raw 10.0" stEvt:changed="/metadata"/> <rdf:li stEvt:action="saved" stEvt:instanceID="xmp.iid:14282d1f-7831-7043-ad77-1e10959ecd50" stEvt:when="2020-04-06T00:55:07+08:00" stEvt:softwareAgent="Adobe Photoshop Camera Raw (Windows)" stEvt:changed="/metadata"/> </rdf:Seq> </xmpMM:History> <Iptc4xmpCore:CreatorContactInfo Iptc4xmpCore:CiTelWork="123456" Iptc4xmpCore:CiEmailWork="123456@gmail.com" Iptc4xmpCore:CiUrlWork="www.123456.com"/> </rdf:Description> </rdf:RDF> </x:xmpmeta>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 <?xpacket end="w"?>
""".strip('\n')
