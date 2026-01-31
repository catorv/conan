#pragma once

#include <vector>
#include <string>

{% set define_name = package_name.upper() %}
#ifdef _WIN32
  #define {{define_name}}_EXPORT __declspec(dllexport)
#else
  #define {{define_name}}_EXPORT
#endif

{{define_name}}_EXPORT void {{package_name}}();
{{define_name}}_EXPORT void {{package_name}}_print_vector(const std::vector<std::string> &strings);
