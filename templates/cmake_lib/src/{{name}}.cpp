#include "{{name}}/{{name}}.h"
#include <iostream>
{% if requires is defined -%}
{% for require in requires -%}
#include "{{ as_name(require) }}.h"
{% endfor %}
{%- endif %}


void {{package_name}}(){
  {% if requires is defined -%}
  {% for require in requires -%}
  {{ as_name(require).replace(".", "_") }}();
  {% endfor %}
  {%- endif %}

#ifdef NDEBUG
  std::cout << "{{name}}/{{version}}: Hello World Release!\n";
#else
  std::cout << "{{name}}/{{version}}: Hello World Debug!\n";
#endif
}

void {{package_name}}_print_vector(const std::vector<std::string> &strings) {
  for(std::vector<std::string>::const_iterator it = strings.begin(); it != strings.end(); ++it) {
    std::cout << "{{package_name}}/{{version}} " << *it << std::endl;
  }
}
