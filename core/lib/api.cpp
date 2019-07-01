#include <exiv2/exiv2.hpp>

#include <iostream>
#include <iomanip>
#include <cassert>

#include <stdlib.h>
#include <string>
#include <sstream>

#define DLLEXPORT extern "C" __declspec(dllexport)

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

DLLEXPORT char *modify_exif(char *const buffer) try
{
	Exiv2::ExifData &exifData = image->exifData();
	// Exiv2::ExifData exifData;	// an empty container for exif metadata

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

		// delete the key if the value is empty
		if (value == "")
		{
			Exiv2::ExifData::iterator pos = exifData.findKey(Exiv2::ExifKey(key));
			if (pos != exifData.end())
				exifData.erase(pos);
			else
				; // throw Exiv2::Error(Exiv2::kerErrorMessage, "Key not found");
			continue;
		}

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

DLLEXPORT char *modify_iptc(char *const buffer) try
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

		// delete the key if the value is empty
		if (value == "")
		{
			Exiv2::IptcData::iterator pos = iptcData.findKey(Exiv2::IptcKey(key));
			if (pos != iptcData.end())
				iptcData.erase(pos);
			else
				; // throw Exiv2::Error(Exiv2::kerErrorMessage, "Key not found");
			continue;
		}

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

DLLEXPORT char *modify_xmp(char *const buffer) try
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

		// delete the key if the value is empty
		if (value == "")
		{
			Exiv2::XmpData::iterator pos = xmpData.findKey(Exiv2::XmpKey(key));
			if (pos != xmpData.end())
				xmpData.erase(pos);
			else
				; // throw Exiv2::Error(Exiv2::kerErrorMessage, "Key not found");
			continue;
		}

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
