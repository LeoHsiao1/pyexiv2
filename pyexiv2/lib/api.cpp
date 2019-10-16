#include <exiv2/exiv2.hpp>

#include <string>
#include <sstream>

// #define API extern "C" // on Linux
#define API extern "C" __declspec(dllexport) // on Windows

// Define some duplicate code
#define catch_block                       \
	catch (Exiv2::Error & e)              \
	{                                     \
		std::stringstream ss;             \
		ss << EXCEPTION_HINT << e.what(); \
		ret = ss.str();                   \
		return ret.c_str();               \
	}

#define read_block                                             \
	{                                                          \
		std::stringstream ss;                                  \
		for (; i != end; ++i)                                  \
		{                                                      \
			ss << i->key() << SEP;                             \
                                                               \
			const char *typeName = i->typeName();              \
			ss << (typeName ? typeName : "Unknown") << SEP;    \
                                                               \
			std::stringstream _value;                          \
			_value << i->value();                              \
			std::string _str = _value.str();                   \
			ss << replace_all(_str, EOL, EOL_replaced) << EOL; \
		}                                                      \
		ret = ss.str();                                        \
		return ret.c_str();                                    \
	}

#define parse_block                                 \
	{                                               \
		/* locate a line */                         \
		EOL_pos = text.find(EOL, pos);              \
		if (EOL_pos == text.npos)                   \
			break;                                  \
                                                    \
		/* get key */                               \
		SEP_pos = text.find(SEP, pos);              \
		key = text.substr(pos, SEP_pos - pos);      \
		pos = SEP_pos + SEP.length();               \
                                                    \
		/* get typeName */                          \
		SEP_pos = text.find(SEP, pos);              \
		typeName = text.substr(pos, SEP_pos - pos); \
		pos = SEP_pos + SEP.length();               \
                                                    \
		/* get value */                             \
		value = text.substr(pos, EOL_pos - pos);    \
		pos = EOL_pos + EOL.length();               \
	}

const std::string SEP = "\t";
const std::string EOL = "\v\f";
const std::string EOL_replaced = "\v\b";
const std::string COMMA = ", ";
const char *EXCEPTION_HINT = "(Caught Exiv2 exception) ";
const char *OK = "OK";
Exiv2::Image::AutoPtr image;  // Cache the image, to avoid the time it takes to open it repeatedly
std::string ret; // Cache the return value

// Replace the substring repeatedly
std::string &replace_all(std::string &str, const std::string &src, const std::string &dest)
{
	while (true)
	{
		std::string::size_type pos(0);
		if ((pos = str.find(src)) != std::string::npos)
			str.replace(pos, src.length(), dest);
		else
			break;
	}
	return str;
}

API const char *open_image(const char *file) try
{
	image = Exiv2::ImageFactory::open(file);
	if (image.get() == 0)
	{
		throw Exiv2::Error(Exiv2::kerErrorMessage, "Can not open the file.");
	}
	image->readMetadata();
	return OK;
}
catch_block;

API const char *read_exif(void) try
{
	Exiv2::ExifData &data = image->exifData();
	Exiv2::ExifData::iterator i = data.begin();
	Exiv2::ExifData::iterator end = data.end();
	read_block;
}
catch_block;

API const char *read_iptc(void) try
{
	Exiv2::IptcData &data = image->iptcData();
	Exiv2::IptcData::iterator i = data.begin();
	Exiv2::IptcData::iterator end = data.end();
	read_block;
}
catch_block;


API const char *read_xmp(void) try
{
	Exiv2::XmpData &data = image->xmpData();
	Exiv2::XmpData::iterator i = data.begin();
	Exiv2::XmpData::iterator end = data.end();
	read_block;
}
catch_block;

API const char *read_raw_xmp(void) try
{
	ret = image->xmpPacket();
	if (ret.empty())
		return OK;
	return ret.c_str();
}
catch_block;

API const char *modify_exif(const char *buffer) try
{
	Exiv2::ExifData &exifData = image->exifData();
	std::string text(buffer);
	int pos = 0;
	int SEP_pos = 0;
	int EOL_pos = 0;
	std::string key = "";
	std::string typeName = "";
	std::string value = "";
	while (pos < text.length())
	{
		parse_block;

		Exiv2::ExifData::iterator key_pos = exifData.findKey(Exiv2::ExifKey(key));
		if (key_pos != exifData.end())
			exifData.erase(key_pos);
		if (value == "")
			continue;   // delete the tag if value == ""
		exifData[key] = value;
	}
	image->setExifData(exifData);
	image->writeMetadata();
	return OK;
}
catch_block;

API const char *modify_iptc(const char *buffer) try
{
	Exiv2::IptcData &iptcData = image->iptcData();
	std::string text(buffer);
	int pos = 0;
	int SEP_pos = 0;
	int EOL_pos = 0;
	std::string key = "";
	std::string typeName = "";
	std::string value = "";
	while (pos < text.length())
	{
		parse_block;

		Exiv2::IptcData::iterator key_pos = iptcData.findKey(Exiv2::IptcKey(key));
		if (key_pos != iptcData.end())
			iptcData.erase(key_pos);
		if (value == "")
			continue;
		iptcData[key] = value;
	}
	image->setIptcData(iptcData);
	image->writeMetadata();
	return OK;
}
catch_block;

API const char *modify_xmp(const char *buffer) try
{
	Exiv2::XmpData &xmpData = image->xmpData();
	std::string text(buffer);
	int pos = 0;
	int SEP_pos = 0;
	int EOL_pos = 0;
	std::string key = "";
	std::string typeName = "";
	std::string value = "";
	while (pos < text.length())
	{
		parse_block;

		Exiv2::XmpData::iterator key_pos = xmpData.findKey(Exiv2::XmpKey(key));
		if (key_pos != xmpData.end())
			xmpData.erase(key_pos);
		if (value == "")
			continue;

		// Handling array types
		if (typeName == "array")
		{
			int __pos = 0;
			int COMMA_pos = 0;
			while (COMMA_pos != std::string::npos)
			{
				COMMA_pos = value.find(COMMA, __pos);
				xmpData[key] = value.substr(__pos, COMMA_pos - __pos);
				__pos = COMMA_pos + COMMA.length();
			}
		}
		else
			xmpData[key] = value;
	}
	image->setXmpData(xmpData);
	image->writeMetadata();
	return OK;
}
catch_block;

API const char *clear_exif(void) try
{
	Exiv2::ExifData exifData; // an empty container for exif metadata
	image->setExifData(exifData);
	image->writeMetadata();
	return OK;
}
catch_block;

API const char *clear_iptc(void) try
{
	Exiv2::IptcData iptcData;
	image->setIptcData(iptcData);
	image->writeMetadata();
	return OK;
}
catch_block;

API const char *clear_xmp(void) try
{
	Exiv2::XmpData xmpData;
	image->setXmpData(xmpData);
	image->writeMetadata();
	return OK;
}
catch_block;