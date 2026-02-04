cmake_minimum_required(VERSION 3.15)
project({{name}} CXX)

include_directories(
    ${PROJECT_SOURCE_DIR}/include/
)

{% if requires is defined -%}
{% for require in requires -%}
find_package({{as_name(require)}} CONFIG REQUIRED)
{% endfor %}
{%- endif %}

add_executable({{name}} src/{{name}}.cpp src/main.cpp)

{% if requires is defined -%}
{% for require in requires -%}
target_link_libraries({{name}} PRIVATE {{as_name(require)}}::{{as_name(require)}})
{% endfor %}
{%- endif %}

install(TARGETS {{name}} DESTINATION "."
    RUNTIME DESTINATION bin
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
)

