#include <iostream>
#include <vector>
#include <string>
#include <map>

#ifndef FORMATTER_HPP
#define FORMATTER_HPP

namespace Formatter
{

    const char CHR_PLACEHOLDER = '$';

    const std::vector<char> EOLS = {
        ')',
        '(',
        '{',
        '}',
        ';',
        ' ',
    };

    std::string formatQuery(std::string, std::map<std::string, std::string>);

}

#endif