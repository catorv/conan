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
