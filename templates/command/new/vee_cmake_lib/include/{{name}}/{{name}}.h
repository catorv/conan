#pragma once

{% set define_name = package_name.upper() %}
#ifdef _WIN32
  #define {{define_name}}_EXPORT __declspec(dllexport)
#else
  #define {{define_name}}_EXPORT
#endif

{{define_name}}_EXPORT void {{package_name}}();

