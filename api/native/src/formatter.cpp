#include <iostream>
#include <algorithm>
#include <string>
#include <regex>
#include <map>

#include "../include/formatter.hpp"

std::string Formatter::formatQuery(std::string query, std::map<std::string, std::string> values)
{
    int index = 0;
    const int len = query.size();

    for (int i = 0; i < len; i++)
    {
        char c = query[i];

        if (index == 0 && c == Formatter::CHR_PLACEHOLDER)
        {
            index = i;
        }
        if (index != 0)
        {
            if (i == len - 1 || (std::find(EOLS.begin(), EOLS.end(), c)) != EOLS.end())
            {
                int count = i - index;
                if (i == len - 1)
                    count++;

                std::string placeholder = query.substr(index, count);

                query.replace(index, count, values[placeholder.substr(1, placeholder.size())]);
                index = 0;
            }
        }
    }
    return query;
}