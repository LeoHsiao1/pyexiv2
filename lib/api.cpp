#include <exiv2/exiv2.hpp>

#include <iostream>
#include <iomanip>
#include <cassert>

#include <stdlib.h>
#include <string>
#include <sstream>

#define DLLEXPORT extern "C" __declspec(dllexport)


char *buffer = NULL;


DLLEXPORT int free_buffer(void)
{
	if(buffer != NULL){
		free(buffer);
		buffer = NULL;
	}
	return 0;
}


// Convert string to char array
char *make_buffer(std::string str)
{
	if(buffer != NULL) free_buffer();
	
	char *buffer=(char *)malloc(str.length());	// must free it later by free_buffer()
	memset(buffer, 0, str.length());
	strcpy(buffer, str.c_str());
	return buffer;
}


DLLEXPORT char *exif(char *const file)
try {
	// open the picture
    Exiv2::Image::AutoPtr image = Exiv2::ImageFactory::open(file);
    assert(image.get() != 0);
	if (image.get() == 0){
		std::string error("Can not open the file");
        throw Exiv2::Error(Exiv2::kerErrorMessage, error);
	}
    
	// read metadata
	image->readMetadata();
    Exiv2::ExifData &exifData = image->exifData();
    if (exifData.empty()){
		std::string error("No Exif data found in file");
        throw Exiv2::Error(Exiv2::kerErrorMessage, error);
	}

	// make the data to JSON format
    std::stringstream json;
	json << "{";
	Exiv2::ExifData::const_iterator end = exifData.end();
    for (Exiv2::ExifData::const_iterator i = exifData.begin(); i != end; ++i) {
		const char* type = i->typeName();
        json << "\""<< i->key() << "\":"
			 // << "\""<< std::dec << i->value()<< "\" ,";
			 << "\"" << i->value()<< "\",";
    }
	json << "\"__status\":0"
		 << "}";

	return make_buffer(json.str());
}
catch (Exiv2::Error& e) {
	std::stringstream error;
	error << "(Caught Exiv2 exception) " << e.what();
	return make_buffer(error.str());
}
