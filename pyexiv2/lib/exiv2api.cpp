#include <pybind11/pybind11.h>
#include <exiv2/exiv2.hpp>
#include <string>
#include <sstream>
#include <iostream>

namespace py = pybind11;
const std::string COMMA = ", ";
const char *EXCEPTION_HINT = "Caught Exiv2 exception: ";
std::stringstream error_log;

class Buffer{
public:
    char *data;
    long size;

    Buffer(const char *data_, long size_){
        size = size_;
        data = (char *)calloc(size, sizeof(char));
        if(data == NULL)
            throw std::runtime_error("Failed to allocate memory.");
        memcpy(data, data_, size);
    }

    void destroy(){
        if(data){
            // std::cout << "deleting" << data << std::endl;
            free(data);
            data = NULL;
        }
    }

    py::bytes dump(){
        return py::bytes((char *)data, size);
    }
};

void check_error_log()
{
    std::string str = error_log.str();
    if(str != ""){
        error_log.clear();  // Clear it so it can be used again
        error_log.str("");
        throw std::runtime_error(str);
    }
}

void logHandler(int level, const char *msg)
{
    switch (level)
    {
    case Exiv2::LogMsg::debug:
    case Exiv2::LogMsg::info:
    case Exiv2::LogMsg::warn:
        std::cout << msg << std::endl;
        break;

    case Exiv2::LogMsg::error:
        // For unknown reasons, the exception thrown here cannot be caught, so save the log to error_log
        // throw std::exception(msg);
        error_log << msg;
        break;

    default:
        return;
    }
}

void set_log_level(int level)
{
    if (level == 0)
        Exiv2::LogMsg::setLevel(Exiv2::LogMsg::debug);
    if (level == 1)
        Exiv2::LogMsg::setLevel(Exiv2::LogMsg::info);
    if (level == 2)
        Exiv2::LogMsg::setLevel(Exiv2::LogMsg::warn);
    if (level == 3)
        Exiv2::LogMsg::setLevel(Exiv2::LogMsg::error);
    if (level == 4)
        Exiv2::LogMsg::setLevel(Exiv2::LogMsg::mute);
}

void init()
{
    Exiv2::LogMsg::setHandler(logHandler);
}

#define read_block                                                     \
    {                                                                  \
        py::list table;                                                \
        for (; i != end; ++i)                                          \
        {                                                              \
            py::list line;                                             \
            line.append(py::bytes(i->key()));                          \
                                                                       \
            std::stringstream _value;                                  \
            _value << i->value();                                      \
            line.append(py::bytes(_value.str()));                      \
                                                                       \
            const char *typeName = i->typeName();                      \
            line.append(py::bytes((typeName ? typeName : "Unknown"))); \
            table.append(line);                                        \
        }                                                              \
        check_error_log();                                             \
        return table;                                                  \
    }

class Image{
public:
    Exiv2::Image::AutoPtr *img = new Exiv2::Image::AutoPtr;

    Image(const char *filename){
        *img = Exiv2::ImageFactory::open(filename);
        if (img->get() == 0)
            throw Exiv2::Error(Exiv2::kerErrorMessage, "Can not open this image.");
        (*img)->readMetadata();
        check_error_log();
    }

    Image(Buffer buffer){
        *img = Exiv2::ImageFactory::open((Exiv2::byte *)buffer.data, buffer.size);
        if (img->get() == 0)
            throw Exiv2::Error(Exiv2::kerErrorMessage, "Can not open this image.");
        (*img)->readMetadata();
        check_error_log();
    }

    void close_image()
    {
        delete img;
        check_error_log();
    }

    py::bytes get_bytes_of_image()
    {
        Exiv2::BasicIo &io = (*img)->io();
        return py::bytes((char *)io.mmap(), io.size());
    }

    py::object read_exif()
    {
        Exiv2::ExifData &data = (*img)->exifData();
        Exiv2::ExifData::iterator i = data.begin();
        Exiv2::ExifData::iterator end = data.end();
        read_block;
    }

    py::object read_iptc()
    {
        Exiv2::IptcData &data = (*img)->iptcData();
        Exiv2::IptcData::iterator i = data.begin();
        Exiv2::IptcData::iterator end = data.end();
        read_block;
    }

    py::object read_xmp()
    {
        Exiv2::XmpData &data = (*img)->xmpData();
        Exiv2::XmpData::iterator i = data.begin();
        Exiv2::XmpData::iterator end = data.end();
        read_block;
    }

    py::object read_raw_xmp()
    {
        return py::bytes((*img)->xmpPacket());
    }

    py::object read_comment()
    {
        return py::bytes((*img)->comment());
    }

    void modify_exif(py::list table, py::str encoding)
    {
        Exiv2::ExifData &exifData = (*img)->exifData();
        for (auto _line : table){
            py::list line;
            for (auto item : _line)
                line.append(item);          // can't use item[0] here, so convert to py::list
            std::string key = py::bytes(line[0].attr("encode")(encoding));
            std::string value = py::bytes(line[1].attr("encode")(encoding));

            Exiv2::ExifData::iterator key_pos = exifData.findKey(Exiv2::ExifKey(key));
            if (key_pos != exifData.end())
                exifData.erase(key_pos);    // delete the existing tag to write a value
            if (value == "")
                continue;                   // skip the tag if value == ""
            exifData[key] = value;          // write a value to the tag
        }
        (*img)->setExifData(exifData);
        (*img)->writeMetadata();
        check_error_log();
    }

    void modify_iptc(py::list table, py::str encoding)
    {
        Exiv2::IptcData &iptcData = (*img)->iptcData();
        for (auto _line : table){
            py::list line;
            for (auto item : _line)
                line.append(item);
            std::string key = py::bytes(line[0].attr("encode")(encoding));
            std::string value = py::bytes(line[1].attr("encode")(encoding));
            std::string typeName = py::bytes(line[2].attr("encode")(encoding));

            Exiv2::IptcData::iterator key_pos = iptcData.findKey(Exiv2::IptcKey(key));
            while (key_pos != iptcData.end()){  // use the while loop because the iptc key may repeat
                iptcData.erase(key_pos);
                key_pos = iptcData.findKey(Exiv2::IptcKey(key));
            }
            if (value == "")
                continue;

            if (typeName == "array")
            {
                Exiv2::Value::AutoPtr exiv2_value = Exiv2::Value::create(Exiv2::string);
                int pos = 0;
                int COMMA_pos = 0;
                while (COMMA_pos != std::string::npos)
                {
                    COMMA_pos = value.find(COMMA, pos);
                    exiv2_value->read(value.substr(pos, COMMA_pos - pos));
                    iptcData.add(Exiv2::IptcKey(key), exiv2_value.get());
                    pos = COMMA_pos + COMMA.length();
                }
            }
            else
                iptcData[key] = value;
        }
        (*img)->setIptcData(iptcData);
        (*img)->writeMetadata();
        check_error_log();
    }

    void modify_xmp(py::list table, py::str encoding)
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
        check_error_log();
    }

    void modify_comment(py::str data, py::str encoding)
    {
        std::string comment = py::bytes(data.attr("encode")(encoding));
        (*img)->setComment(comment);
        (*img)->writeMetadata();
        check_error_log();
    }

    void clear_exif()
    {
        Exiv2::ExifData exifData;   // create an empty container of exif metadata
        (*img)->setExifData(exifData);
        (*img)->writeMetadata();
        check_error_log();
    }

    void clear_iptc()
    {
        Exiv2::IptcData iptcData;
        (*img)->setIptcData(iptcData);
        (*img)->writeMetadata();
        check_error_log();
    }

    void clear_xmp()
    {
        Exiv2::XmpData xmpData;
        (*img)->setXmpData(xmpData);
        (*img)->writeMetadata();
        check_error_log();
    }

    void clear_comment()
    {
        (*img)->clearComment();
        (*img)->writeMetadata();
        check_error_log();
    }
};

PYBIND11_MODULE(exiv2api, m)
{
    m.doc() = "Expose the API of exiv2 to Python.";
    m.def("set_log_level", &set_log_level);
    m.def("init"         , &init);
    py::class_<Buffer>(m, "Buffer")
        .def(py::init<const char *, long>())
        .def_readonly("data"      , &Buffer::data)
        .def_readonly("size"      , &Buffer::size)
        .def("destroy"            , &Buffer::destroy)
        .def("dump"               , &Buffer::dump);
    py::class_<Image>(m, "Image")
        .def(py::init<const char *>())
        .def(py::init<Buffer &>())
        .def("close_image"       , &Image::close_image)
        .def("get_bytes_of_image", &Image::get_bytes_of_image)
        .def("read_exif"         , &Image::read_exif)
        .def("read_iptc"         , &Image::read_iptc)
        .def("read_xmp"          , &Image::read_xmp)
        .def("read_raw_xmp"      , &Image::read_raw_xmp)
        .def("read_comment"      , &Image::read_comment)
        .def("modify_exif"       , &Image::modify_exif)
        .def("modify_iptc"       , &Image::modify_iptc)
        .def("modify_xmp"        , &Image::modify_xmp)
        .def("modify_comment"    , &Image::modify_comment)
        .def("clear_exif"        , &Image::clear_exif)
        .def("clear_iptc"        , &Image::clear_iptc)
        .def("clear_xmp"         , &Image::clear_xmp)
        .def("clear_comment"     , &Image::clear_comment);
}
