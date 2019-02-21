#pragma once

#include <string>
#include <map>
#include <vector>

namespace cpputil {
namespace program{

class Conf {
public:
    Conf(const std::string & filename){
        parse(filename, _options);
        resolve_reference();
    }

    std::string get(const std::string & key, const std::string & default_value = "") const;

    // 3参数版本(non-const) 将废弃
    std::string get(const std::string & key, const std::string & default_value,
            bool resolve_ref) __attribute__ ((deprecated));

    std::vector<std::string> get_values(const std::string & key, bool clean_empty = false) const;

    std::map<std::string, std::string> get_all() const;

private:
    void parse(const std::string & filename, std::map<std::string, std::string> & options);
    void resolve_reference();
    void resolve_reference(const std::string & key);

    std::map<std::string, std::string> _options;
    //messages during parsing
    std::vector<std::string> _messages;
};

} /* namespace program */
} /* namespace cpputil */

