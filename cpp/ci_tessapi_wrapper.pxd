from libcpp.string cimport string

# Declare the class with cdef
cdef extern from "ci_tessapi_wrapper.h":
    cdef cppclass CITessApiWrapper:
        CITessApiWrapper() except +
        string eng_image_to_string(unsigned char *, unsigned int, unsigned int,
                                 string, int, int)
        string gs_image_to_string(unsigned char *, unsigned int, unsigned int,
                                 string, int, int)