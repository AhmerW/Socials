#include <iostream>
#include <map>

#include "include/formatter.hpp"

int main()
{
    std::string query = "select * from x where test = $test or z in $z and $test orr $test $z $x";
    std::map<std::string, std::string> values = {{"test", "10"}, {"z", "5"}, {"x", "oo"}};

    std::cout << Formatter::formatQuery(query, values) << std::endl;

    return 0;
}