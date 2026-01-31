#include "{{name}}/{{name}}.h"
#include <vector>
#include <string>

int main() {
    {{package_name}}();

    std::vector<std::string> vec;
    vec.push_back("test_package");

    {{package_name}}_print_vector(vec);
}

