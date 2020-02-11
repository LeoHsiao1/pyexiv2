#include <pybind11/pybind11.h>
#include <exiv2/exiv2.hpp>
#include <string>

namespace py = pybind11;
py::object OK = py::str("OK");
const std::string COMMA = ", ";


py::object open_image(const char *filename) 
{
    Exiv2::Image::AutoPtr *img = new Exiv2::Image::AutoPtr;
    *img = Exiv2::ImageFactory::open(filename);
    if (img->get() == 0)
        throw Exiv2::Error(Exiv2::kerErrorMessage, "Can not open this file.");
    (*img)->readMetadata();
    return py::cast(img);
}

py::object close_image(Exiv2::Image::AutoPtr *img)
{
    delete img;
    return OK;
    // Do not operate on the closed image.
}

#define read_block                                                      \
	{                                                                   \
        py::list table;                                                 \
        for (; i != end; ++i)                                           \
        {                                                               \
            py::list line;                                              \
            line.append(py::bytes(i->key()));                           \
                                                                        \
            std::stringstream _value;                                   \
            _value << i->value();                                       \
            line.append(py::bytes(_value.str()));                       \
                                                                        \
            const char *typeName = i->typeName();                       \
            line.append(py::bytes((typeName ? typeName : "Unknown")));  \
            table.append(line);                                         \
        }                                                               \
        return table;                                                   \
	}

py::object read_exif(Exiv2::Image::AutoPtr *img)
{
    Exiv2::ExifData &data = (*img)->exifData();
    Exiv2::ExifData::iterator i = data.begin();
    Exiv2::ExifData::iterator end = data.end();
    read_block;
}

py::object read_iptc(Exiv2::Image::AutoPtr *img)
{
	Exiv2::IptcData &data = (*img)->iptcData();
	Exiv2::IptcData::iterator i = data.begin();
	Exiv2::IptcData::iterator end = data.end();
	read_block;
}

py::object read_xmp(Exiv2::Image::AutoPtr *img)
{
	Exiv2::XmpData &data = (*img)->xmpData();
	Exiv2::XmpData::iterator i = data.begin();
	Exiv2::XmpData::iterator end = data.end();
	read_block;
}

py::object read_raw_xmp(Exiv2::Image::AutoPtr *img)
{
	return py::bytes((*img)->xmpPacket());
}

py::object modify_exif(Exiv2::Image::AutoPtr *img, py::list table, py::str encoding)
{
	Exiv2::ExifData &exifData = (*img)->exifData();
    for (auto _line : table){
        py::list line;
        for (auto item : _line)
            line.append(item);  // can't use item[0] here, so convert to py::list
        std::string key = py::bytes(line[0].attr("encode")(encoding));
        std::string value = py::bytes(line[1].attr("encode")(encoding));

        Exiv2::ExifData::iterator key_pos = exifData.findKey(Exiv2::ExifKey(key));
		if (key_pos != exifData.end())
			exifData.erase(key_pos);
		if (value == "")
			continue;   // delete the tag if value == ""
		exifData[key] = value;
	}
	(*img)->setExifData(exifData);
	(*img)->writeMetadata();
	return OK;
}

py::object modify_iptc(Exiv2::Image::AutoPtr *img, py::list table, py::str encoding)
{
	Exiv2::IptcData &iptcData = (*img)->iptcData();
    for (auto _line : table){
        py::list line;
        for (auto item : _line)
            line.append(item);
        std::string key = py::bytes(line[0].attr("encode")(encoding));
        std::string value = py::bytes(line[1].attr("encode")(encoding));

        Exiv2::IptcData::iterator key_pos = iptcData.findKey(Exiv2::IptcKey(key));
		if (key_pos != iptcData.end())
			iptcData.erase(key_pos);
		if (value == "")
			continue;
		iptcData[key] = value;
	}
	(*img)->setIptcData(iptcData);
	(*img)->writeMetadata();
	return OK;
}

py::object modify_xmp(Exiv2::Image::AutoPtr *img, py::list table, py::str encoding)
{
	Exiv2::XmpData &xmpData = (*img)->xmpData();
    for (auto _line : table){
        py::list line;
        for (auto item : _line)
            line.append(item);
        std::string key = py::bytes(line[0].attr("encode")(encoding));
        std::string value = py::bytes(line[1].attr("encode")(encoding));
        std::string typeName = py::bytes(line[2].attr("encode")(encoding));
        
        Exiv2::XmpData::iterator key_pos = xmpData.findKey(Exiv2::XmpKey(key));
		if (key_pos != xmpData.end())
			xmpData.erase(key_pos);
		if (value == "")
			continue;

        if (typeName == "array")
		{
            // Handling the value of array types
            int pos = 0;
			int COMMA_pos = 0;
			while (COMMA_pos != std::string::npos)
			{
				COMMA_pos = value.find(COMMA, pos);
				xmpData[key] = value.substr(pos, COMMA_pos - pos);
				pos = COMMA_pos + COMMA.length();
			}
        }
        else
            xmpData[key] = value;
    }
	(*img)->setXmpData(xmpData);
	(*img)->writeMetadata();
	return OK;
}

py::object clear_exif(Exiv2::Image::AutoPtr *img)
{
	Exiv2::ExifData exifData; // an empty container of exif metadata
	(*img)->setExifData(exifData);
	(*img)->writeMetadata();
	return OK;
}

py::object clear_iptc(Exiv2::Image::AutoPtr *img)
{
	Exiv2::IptcData iptcData;
	(*img)->setIptcData(iptcData);
	(*img)->writeMetadata();
	return OK;
}

py::object clear_xmp(Exiv2::Image::AutoPtr *img)
{
	Exiv2::XmpData xmpData;
	(*img)->setXmpData(xmpData);
	(*img)->writeMetadata();
	return OK;
}

PYBIND11_MODULE(api, m)
{
    m.doc() = "Expose the API of exiv2 to Python.";
    py::class_<Exiv2::Image::AutoPtr>(m, "Exiv2_Image_AutoPtr")
        .def(py::init<>());
    m.def("open_image", &open_image);
    m.def("close_image", &close_image);
    m.def("read_exif", &read_exif);
    m.def("read_iptc", &read_iptc);
    m.def("read_xmp", &read_xmp);
    m.def("read_raw_xmp", &read_raw_xmp);
    m.def("modify_exif", &modify_exif);
    m.def("modify_iptc", &modify_iptc);
    m.def("modify_xmp", &modify_xmp);
    m.def("clear_exif", &clear_exif);
    m.def("clear_iptc", &clear_iptc);
    m.def("clear_xmp", &clear_xmp);
}
