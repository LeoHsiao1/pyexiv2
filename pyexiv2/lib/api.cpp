#include <exiv2/exiv2.hpp>

#include <iostream>
#include <iomanip>
#include <cassert>

#include <stdlib.h>
#include <string>
#include <sstream>

#define API extern "C" // on Linux
//#define API extern "C" __declspec(dllexport) // on Windows

char *buffer = 0;
Exiv2::Image::AutoPtr image;
std::string SEP("\t"); // separator
std::string EOL("<<SEPARATOR>>\n");
char ZERO = '0';

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

API char *open_image(char *const file) try
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

API char *read_exif(void) try
{
	Exiv2::ExifData &exifData = image->exifData();
	std::stringstream data;
	Exiv2::ExifData::iterator end = exifData.end();
	for (Exiv2::ExifData::iterator i = exifData.begin(); i != end; ++i)
	{
		//add data with separators
		data << i->key() << "\t"
			 << i->value() << "<<SEPARATOR>>\n";
			 //<< i->typeName() << "\t"	// Some metadata does not have this property, causing the program to crash
	}
	return make_buffer(data.str());
}
catch (Exiv2::Error &e)
{
	std::stringstream error;
	error << "(Caught Exiv2 exception) " << e.what();
	return make_buffer(error.str());
}

API char *read_iptc(void) try
{
	Exiv2::IptcData &iptcData = image->iptcData();
	std::stringstream data;
	Exiv2::IptcData::iterator end = iptcData.end();
	for (Exiv2::IptcData::iterator i = iptcData.begin(); i != end; ++i)
	{
		data << i->key() << "\t"
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

API char *read_xmp(void) try
{
	Exiv2::XmpData &xmpData = image->xmpData();
	std::stringstream data;
	Exiv2::XmpData::iterator end = xmpData.end();
	for (Exiv2::XmpData::iterator i = xmpData.begin(); i != end; ++i)
	{
		data << i->key() << "\t"
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

API char *clear_exif(void) try
{
	Exiv2::ExifData exifData; // an empty container for exif metadata
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

API char *clear_iptc(void) try
{
	Exiv2::IptcData iptcData;
	image->setIptcData(iptcData);
	image->writeMetadata();
	return &ZERO;
}
catch (Exiv2::Error &e)
{
	std::stringstream error;
	error << "(Caught Exiv2 exception) " << e.what();
	return make_buffer(error.str());
}

API char *clear_xmp(void) try
{
	Exiv2::XmpData xmpData;
	image->setXmpData(xmpData);
	image->writeMetadata();
	return &ZERO;
}
catch (Exiv2::Error &e)
{
	std::stringstream error;
	error << "(Caught Exiv2 exception) " << e.what();
	return make_buffer(error.str());
}

API char *modify_exif(char *const buffer) try
{
	Exiv2::ExifData &exifData = image->exifData();
	std::string text(buffer);
	int i = 0; // current index in the text
	int SEP_pos = 0;
	int EOL_pos = 0;
	std::string key = "";
	std::string value = "";
	while (i < text.length())
	{
		// locate a line
		EOL_pos = text.find(EOL, i);
		if (EOL_pos == text.npos)
			break;

		// get the first field for each row
		SEP_pos = text.find(SEP, i);
		key = text.substr(i, SEP_pos - i);
		i = SEP_pos + SEP.length();

		// get the second field for each row
		value = text.substr(i, EOL_pos - i);
		i = EOL_pos + EOL.length();

		Exiv2::ExifData::iterator pos = exifData.findKey(Exiv2::ExifKey(key));
		if (pos != exifData.end())
			exifData.erase(pos);
		// else
		// throw Exiv2::Error(Exiv2::kerErrorMessage, "Key not found");
		if (value != "")
			exifData[key] = value;
	}
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

API char *modify_iptc(char *const buffer) try
{
	Exiv2::IptcData &iptcData = image->iptcData();
	std::string text(buffer);
	int i = 0; // current index in the text
	int SEP_pos = 0;
	int EOL_pos = 0;
	std::string key = "";
	std::string value = "";
	while (i < text.length())
	{
		EOL_pos = text.find(EOL, i);
		if (EOL_pos == text.npos)
			break;

		SEP_pos = text.find(SEP, i);
		key = text.substr(i, SEP_pos - i);
		i = SEP_pos + SEP.length();

		value = text.substr(i, EOL_pos - i);
		i = EOL_pos + EOL.length();

		Exiv2::IptcData::iterator pos = iptcData.findKey(Exiv2::IptcKey(key));
		if (pos != iptcData.end())
			iptcData.erase(pos);
		if (value != "")
			iptcData[key] = value;
	}
	image->setIptcData(iptcData);
	image->writeMetadata();
	return &ZERO;
}
catch (Exiv2::Error &e)
{
	std::stringstream error;
	error << "(Caught Exiv2 exception) " << e.what();
	return make_buffer(error.str());
}

API char *modify_xmp(char *const buffer) try
{
	Exiv2::XmpData &xmpData = image->xmpData();
	std::string text(buffer);
	int i = 0; // current index in the text
	int SEP_pos = 0;
	int EOL_pos = 0;
	std::string key = "";
	std::string value = "";
	while (i < text.length())
	{
		EOL_pos = text.find(EOL, i);
		if (EOL_pos == text.npos)
			break;

		SEP_pos = text.find(SEP, i);
		key = text.substr(i, SEP_pos - i);
		i = SEP_pos + SEP.length();

		value = text.substr(i, EOL_pos - i);
		i = EOL_pos + EOL.length();

		Exiv2::XmpData::iterator pos = xmpData.findKey(Exiv2::XmpKey(key));
		if (pos != xmpData.end())
			xmpData.erase(pos);
		if (value != "")
			xmpData[key] = value;
	}
	image->setXmpData(xmpData);
	image->writeMetadata();
	return &ZERO;
}
catch (Exiv2::Error &e)
{
	std::stringstream error;
	error << "(Caught Exiv2 exception) " << e.what();
	return make_buffer(error.str());
}
