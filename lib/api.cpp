#include <exiv2/exiv2.hpp>

#include <iostream>
#include <iomanip>
#include <cassert>

#include <stdlib.h>
#include <string>
#include <sstream>

#define DLLEXPORT extern "C" __declspec(dllexport)

char *buffer = 0;
char ZERO = '0';
Exiv2::Image::AutoPtr image;


int free_buffer(void)
{
    if (buffer)
    {
        free(buffer);
        buffer = NULL;
    }
    return 0;
}


// Convert string to char array
char *make_buffer(std::string str)
{
    if (buffer)
        free_buffer(); // free it automatically

    buffer = (char *)malloc(str.length());
    memset(buffer, 0, str.length());
    strcpy(buffer, str.c_str());
    return buffer;
}


DLLEXPORT char *open_image(char *const file) try
{
    image = Exiv2::ImageFactory::open(file);
    if (image.get() == 0)
    {
        std::string error("Can not open the file.");
        throw Exiv2::Error(Exiv2::kerErrorMessage, error);
    }

    image->readMetadata();

	return &ZERO;
}
catch (Exiv2::Error &e)
{
    std::stringstream error;
    error << "(Caught Exiv2 exception) " << e.what();
    return make_buffer(error.str());
}


DLLEXPORT char *read_exif(void) try
{
    Exiv2::ExifData &exifData = image->exifData();
    if (exifData.empty())
    {
        std::string error("No Exif data found in the file.");
        throw Exiv2::Error(Exiv2::kerErrorMessage, error);
    }

    std::stringstream data;
    Exiv2::ExifData::const_iterator end = exifData.end();
    for (Exiv2::ExifData::const_iterator i = exifData.begin(); i != end; ++i)
    {
        //add data with separators
        data << i->key() << "\t"
             << i->typeName() << "\t"
             << i->value() << "<<SEPARATOR>>\n";
    }

    return make_buffer(data.str());
}
catch (Exiv2::Error &e)
{
    std::stringstream error;
    error << "(Caught Exiv2 exception) " << e.what();
    return make_buffer(error.str());
}


DLLEXPORT char *read_iptc(void) try
{
    Exiv2::IptcData &iptcData = image->iptcData();
    if (iptcData.empty())
    {
		std::string error("No IPTC data found in the file.");
        throw Exiv2::Error(Exiv2::kerErrorMessage, error);
    }

    std::stringstream data;
    Exiv2::IptcData::iterator end = iptcData.end();
    for (Exiv2::IptcData::iterator i = iptcData.begin(); i != end; ++i)
    {
        //add data with separators
        data << i->key() << "\t"
             << i->typeName() << "\t"
             << i->value() << "<<SEPARATOR>>\n";
    }

    return make_buffer(data.str());
}
catch (Exiv2::Error &e)
{
    std::stringstream error;
    error << "(Caught Exiv2 exception) " << e.what();
    return make_buffer(error.str());
}


DLLEXPORT char *read_xmp(void) try
{
    Exiv2::XmpData &xmpData = image->xmpData();
    if (xmpData.empty())
    {
		std::string error("No XMP data found in the file.");
        throw Exiv2::Error(Exiv2::kerErrorMessage, error);
    }

    std::stringstream data;
    Exiv2::XmpData::const_iterator end = xmpData.end();
    for (Exiv2::XmpData::const_iterator i = xmpData.begin(); i != end; ++i)
    {
        //add data with separators
        data << i->key() << "\t"
             << i->typeName() << "\t"
             << i->value() << "<<SEPARATOR>>\n";
    }

    return make_buffer(data.str());
}
catch (Exiv2::Error &e)
{
    std::stringstream error;
    error << "(Caught Exiv2 exception) " << e.what();
    return make_buffer(error.str());
}


DLLEXPORT char *write_metadata(char *const key_name, char *const value) try
{
	Exiv2::ExifData &exifData = image->exifData();
	// Exiv2::ExifData exifData;	// an empty container for exif metadata
	
	
	Exiv2::AsciiValue::AutoPtr rv(new Exiv2::AsciiValue);
	std::string v_str(value);
    rv->read(v_str);

	std::string k_str(key_name);
	Exiv2::ExifKey key = Exiv2::ExifKey(k_str);
    Exiv2::ExifData::iterator pos = exifData.findKey(key);
	if (pos == exifData.end())
		exifData.add(key, rv.get());
	else
		pos->setValue(rv.get());

	image->setExifData(exifData);
    image->writeMetadata();

    return &ZERO;
}
catch (Exiv2::Error &e)
{
    std::stringstream error;
    error << "(Caught Exiv2 exception) " << e.what();
    return make_buffer(error.str());
}

/* 
DLLEXPORT char *erase_metadata(char *const file, char *const key_name) try
{
    key = Exiv2::ExifKey(*key_name);
	Exiv2::ExifData exifData;
	Exiv2::ExifData::iterator pos = exifData.findKey(key);
	if (pos == exifData.end())
		throw Exiv2::Error(Exiv2::kerErrorMessage, "Key not found");
	else
		exifData.erase(pos);
	
	Exiv2::Image::AutoPtr image = Exiv2::ImageFactory::open(file);
	image->setExifData(exifData);
    image->writeMetadata();
	
    return &ZERO;
}
catch (Exiv2::Error &e)
{
    std::stringstream error;
    error << "(Caught Exiv2 exception) " << e.what();
    return make_buffer(error.str());
}

 */