import re

from .lib import exiv2api


# These tags are used by Windows and encoded in UCS2-LE.
# pyexiv2 will automatically convert encoding formats when reading and writing them.
EXIF_TAGS_ENCODED_IN_UCS2 = [
    'Exif.Image.XPTitle',
    'Exif.Image.XPComment',
    'Exif.Image.XPAuthor',
    'Exif.Image.XPKeywords',
    'Exif.Image.XPSubject',
]

# These tags can be written repeatedly, so there may be multiple values.
# pyexiv2 will convert their values to a list of strings.
IPTC_TAGS_REPEATABLE = [
    'Iptc.Envelope.Destination',
    'Iptc.Envelope.ProductId',
    'Iptc.Application2.ObjectAttribute',
    'Iptc.Application2.Subject',
    'Iptc.Application2.SuppCategory',
    'Iptc.Application2.Keywords',
    'Iptc.Application2.LocationCode',
    'Iptc.Application2.LocationName',
    'Iptc.Application2.ReferenceService',
    'Iptc.Application2.ReferenceDate',
    'Iptc.Application2.ReferenceNumber',
    'Iptc.Application2.Byline',
    'Iptc.Application2.BylineTitle',
    'Iptc.Application2.Contact',
    'Iptc.Application2.Writer',
]


def _parse(table: list, encoding='utf-8') -> dict:
    """
    exiv2api is only responsible for returning the raw metadata, which is then parsed in Python:
    """
    dic = {}
    for line in table:
        tag, value, typeName = line
        tag   = tag.decode(encoding)
        value = value.decode(encoding)
        if typeName in ['XmpBag', 'XmpSeq']:
            value = value.split(', ')
        elif typeName in ['XmpText']:
            # Handle nested array structures in XML. Refer to https://exiv2.org/manpage.html#set_xmp_struct
            if value in ['type="Bag"', 'type="Seq"']:
                value = ['']
        elif typeName in ['LangAlt']:
            # Refer to https://exiv2.org/manpage.html#langalt_values
            if 'lang=' in value:
                fields = re.split(r', (lang="\S+") ', ', ' + value)[1:]
                value  = {language: content for language, content in zip(fields[0::2], fields[1::2])}

        # Convert the values to a list of strings if the tag has multiple values
        pre_value = dic.get(tag)
        if pre_value == None:
            dic[tag] = value
        elif isinstance(pre_value, str):
            dic[tag] = [pre_value, value]
        elif isinstance(pre_value, list):
            dic[tag].append(value)

    return dic


def _parse_detail(raw_data: list, encoding='utf-8') -> dict:
    table = []
    dic_detail = {}
    for tag_detail in raw_data:
        tag      = tag_detail.pop('tag', b'')
        value    = tag_detail.pop('value', b'')
        typeName = tag_detail.get('typeName', '')
        table.append([tag, value, typeName])
        tag = tag.decode(encoding)
        # A tag may be repeated, so avoid saving tag_detail twice
        if not dic_detail.get(tag):
            dic_detail[tag] = tag_detail
    dic = _parse(table, encoding)
    for tag in dic.keys():
        dic_detail[tag]['value'] = dic[tag]
    return dic_detail


def _dumps(dic: dict) -> list:
    """ Convert the metadata from a dict into a text table. """
    table = []
    for tag, value in dic.items():
        tag      = str(tag)
        if value == None:
            typeName = '_delete'
            value    = ''
        elif isinstance(value, (list, tuple)):
            typeName = 'array'
            value    = list(value)
        elif isinstance(value, dict):
            typeName = 'string'
            value    = ', '.join(['{} {}'.format(k,v) for k,v in value.items()])
        else:
            typeName = 'string'
            value    = str(value)
        line = [tag, value, typeName]
        table.append(line)
    return table


def decode_ucs2(text: str) -> str:
    """
    Convert text from UCS2 encoding to UTF8 encoding.
    For example:
    >>> decode_ucs2('116 0 101 0 115 0 116 0')
    'test'
    """
    hex_str = ''.join(['{:02x}'.format(int(i)) for i in text.split()])
    return bytes.fromhex(hex_str).decode('utf-16le')


def encode_ucs2(text: str) -> str:
    """
    Convert text from UTF8 encoding to UCS2 encoding.
    For example:
    >>> encode_ucs2('test')
    '116 0 101 0 115 0 116 0'
    """
    hex_str = text.encode('utf-16le').hex()
    int_list = [int(''.join(i), base=16) for i in zip(*[iter(hex_str)] * 2)]
    return ' '.join([str(i) for i in int_list])


def convert_exif_to_xmp(data: dict, encoding='utf-8') -> dict:
    """ Input EXIF metadata, convert to XMP metadata and return. It works like executing modify_exif() then read_xmp(). """
    data = data.copy()
    for tag in EXIF_TAGS_ENCODED_IN_UCS2:
        value = data.get(tag)
        if value:
            data[tag] = encode_ucs2(value)
    converted_data = exiv2api.convert_exif_to_xmp(_dumps(data), encoding)
    return _parse(converted_data, encoding)


def convert_iptc_to_xmp(data: dict, encoding='utf-8') -> dict:
    """ Input IPTC metadata, convert to XMP metadata and return. It works like executing modify_iptc() then read_xmp(). """
    converted_data = exiv2api.convert_iptc_to_xmp(_dumps(data), encoding)
    return _parse(converted_data, encoding)


def convert_xmp_to_exif(data: dict, encoding='utf-8') -> dict:
    """ Input XMP metadata, convert to EXIF metadata and return. It works like executing modify_xmp() then read_exif(). """
    converted_data = exiv2api.convert_xmp_to_exif(_dumps(data), encoding)
    return _parse(converted_data, encoding)


def convert_xmp_to_iptc(data: dict, encoding='utf-8') -> dict:
    """ Input XMP metadata, convert to IPTC metadata and return. It works like executing modify_xmp() then read_iptc(). """
    converted_data = exiv2api.convert_xmp_to_iptc(_dumps(data), encoding)
    return _parse(converted_data, encoding)
