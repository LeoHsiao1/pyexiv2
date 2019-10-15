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
			const char *typeName = i->typeName();              \
			std::stringstream _ss;                             \
			_ss << i->value();                                 \
			std::string _str = _ss.str();                      \
			ss << i->key() << SEP                              \
			   << (typeName ? typeName : "Unknown") << SEP     \
			   << replace_all(_str, EOL, EOL_replaced) << EOL; \
		}                                                      \
		ret = ss.str();                                        \
		return ret.c_str();                                    \
	}

const std::string SEP = "\t";
const std::string EOL = "\v\f";
const std::string EOL_replaced = "\v\b";
const char *EXCEPTION_HINT = "(Caught Exiv2 exception) ";
const char *OK = "OK";
Exiv2::Image::AutoPtr image;
std::string ret;  // to cache the return valu

// replace the substring repeatedly
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
		std::string error("Can not open the file.");
		throw Exiv2::Error(Exiv2::kerErrorMessage, error);
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

API const char *modify_exif(const char *buffer) try
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
	return OK;
}
catch_block;

API const char *modify_iptc(const char *buffer) try
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
	return OK;
}
catch_block;

API const char *modify_xmp(const char *buffer) try
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
	return OK;
}
catch_block;
