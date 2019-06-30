#include <exiv2/exiv2.hpp>

#include <iostream>
#include <iomanip>
#include <cassert>

#include <stdlib.h>
#include <string>
#include <sstream>

#define DLLEXPORT extern "C" __declspec(dllexport)

char *buffer = 0;

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

DLLEXPORT char *read_exif(char *const file) try
{
    // open the image
    Exiv2::Image::AutoPtr image = Exiv2::ImageFactory::open(file);
    if (image.get() == 0)
    {
        std::string error("Can not open the file.");
        throw Exiv2::Error(Exiv2::kerErrorMessage, error);
    }

    // read metadata
    image->readMetadata();
    Exiv2::ExifData &exifData = image->exifData();
    if (exifData.empty())
    {
        std::string error("No Exif data found in file.");
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

DLLEXPORT char *read_iptc(char *const file) try
{
    // open the image
    Exiv2::Image::AutoPtr image = Exiv2::ImageFactory::open(file);
    if (image.get() == 0)
    {
        std::string error(file);
        error += ": Can not open the file.";
        throw Exiv2::Error(Exiv2::kerErrorMessage, error);
    }

    // read metadata
    image->readMetadata();
    Exiv2::IptcData &iptcData = image->iptcData();
    if (iptcData.empty())
    {
        std::string error(file);
        error += ": No IPTC Metadata found in the file.";
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

DLLEXPORT char *read_xmp(char *const file) try
{
    // open the image
    Exiv2::Image::AutoPtr image = Exiv2::ImageFactory::open(file);
    if (image.get() == 0)
    {
        std::string error(file);
        error += ": Can not open the file.";
        throw Exiv2::Error(Exiv2::kerErrorMessage, error);
    }

    // read metadata
    image->readMetadata();
    Exiv2::XmpData &xmpData = image->xmpData();
    if (xmpData.empty())
    {
        std::string error(file);
        error += ": No XMP Metadata found in the file.";
        throw Exiv2::Error(Exiv2::kerErrorMessage, error);
    }

    // make the data to JSON format
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
