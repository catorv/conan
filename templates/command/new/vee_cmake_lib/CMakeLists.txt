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


add_library({{name}} src/{{name}}.cpp)
target_include_directories({{name}} PUBLIC include)

{% if requires is defined -%}
{% for require in requires -%}
target_link_libraries({{name}} PRIVATE {{as_name(require)}}::{{as_name(require)}})
{% endfor %}
{%- endif %}

set_target_properties({{name}} PROPERTIES PUBLIC_HEADER "include/{{name}}.h")
install(TARGETS {{name}})

