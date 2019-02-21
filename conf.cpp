#include "conf.h"

#include <fstream>
#include <cctype>
#include <iostream>
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>
#include <boost/filesystem.hpp>
#include <boost/algorithm/string/predicate.hpp>
#include <boost/regex.hpp>

using namespace cpputil::program;
using namespace boost::filesystem;
using namespace std;

enum ParseState {
    KEY,
    VALUE,
    COMMENT,
    ESCAPING,
    DEFAULT
};

static bool is_terminator(int c){
    if(c == ':' || c == '='){
        return true;
    }
    return isspace(c);
}

void Conf::parse(const string & filename, map< string, string > & options){
    path filepath(filename);
    filepath = system_complete(filepath);

    if(is_symlink(symlink_status(filepath))){
        //get target file path when filepath is a symlink
        char buf[1024];
        size_t len = readlink(filepath.string().c_str(), buf, sizeof(buf));
        buf[len] = '\0';
        filepath = path(string(buf));
    }

    path dir = filepath.parent_path();
    std::ifstream file(filepath.string().c_str());
    if(!file){
        _messages.push_back("fail to open file: " + filename);
        return;
    }
    const int32_t buf_len = 4096;
    char buf[buf_len];
    string token = "";
    ParseState pre_state = DEFAULT;
    ParseState state = DEFAULT;
    string key;

    int32_t line_num = 1;
    int32_t colum_num = 0;
    bool new_line = false;
    while(!file.eof()){
        file.read(buf, buf_len);
        int32_t count = file.gcount();
        for(int32_t i = 0; i < count; i++){
            if(new_line){
                line_num++;
                colum_num = 0;
                new_line = false;
            }
            colum_num++;

            if(buf[i] == '\n'){
                new_line = true;
            }
            if( state == ESCAPING ){//leave escaping state
                if(buf[i] == '\n'){
                    //escaping for line continuation
                    state = pre_state;
                }else{
                    token.push_back(buf[i]);
                    state = pre_state;
                }
                continue;
            }
            if(buf[i] == '\\'){//enter escaping state
                pre_state = state;
                state = ESCAPING;
                continue;
            }
            if(buf[i] == '#' || buf[i] == ';'){//comment state
                pre_state = state;
                state = COMMENT;
                continue;
            }

            if(buf[i] == '\n'){//meet line end
                if(key.length() == 0 && token.length() && state == KEY){
                    key = token;
                    token = "";
                }
                boost::trim(token);
                if(key.length() > 0){
                    if(key =="include"){
                       if(!boost::starts_with(token, "/")){
                           //an relative path, relative to current dir
                           path abspath = path(dir);
                           abspath = abspath / token;
                           token = abspath.string();
                       }
                       parse(token, options);
                    }else{
                        options[key] = token;
                    }
                }
                token = "";
                key = "";
                pre_state = VALUE;
                state = DEFAULT;
                continue;
            }

            if(state == COMMENT){
                //ignore everything in COMMENT state
                continue;
            }
            if(is_terminator(buf[i])){
                if(state == KEY){//leave KEY state
                    key = token;
                    token = "";
                    pre_state = state;
                    state = DEFAULT;
                }else if(state == VALUE){//leave VALUE state
                    token.push_back(buf[i]);
                    //pre_state = state;
                    //state = DEFAULT;
                    //if(key == "include"){//recursive parsing for include
                    //    parse(token, options);
                    //}else{
                    //    options[key] = token;
                    //}
                    //key = "";
                    //token = "";
                }
                continue;
            }else{
                if(state == DEFAULT){
                    //need to do state transition
                    if(pre_state == KEY){
                        pre_state = state;
                        state = VALUE;
                    }else if(pre_state == KEY){
                        //meet extra character after value, ignore it
                        continue;
                    }else{
                        state = KEY;
                    }
                }
                char c = buf[i];
                if(state == KEY){
                    c = tolower(c);
                }
                token.push_back(c);
            }
        }
    }

    if(key.length() == 0 && token.length() > 0 && state == KEY){
        key = token;
        token = "";
    }
    if(key.length() > 0){
        if(key =="include"){
            if(!boost::starts_with(token, "/")){
                //an relative path, relative to current dir
                path abspath = path(dir);
                abspath = abspath / token;
                token = abspath.string();
            }
            parse(token, options);
        }else{
            options[key] = token;
        }
    }
    file.close();
    // options = cpputil::consul::translate_conf(options, filename);
}

string Conf::get(const string & key, const string & default_value) const {
   string find_key;
   find_key.reserve(key.length());
   for(uint32_t i = 0; i < key.length(); i++){
       find_key.push_back(tolower(key[i]));
   }
   map< string, string >::const_iterator itr = _options.find(find_key);
   if(itr != _options.end()){
       string val = itr->second;
       return val;
   }else{
       return default_value;
   }
}

// 仅供接口兼容使用
string Conf::get(const string & key, const string & default_value, bool resolve_ref) {
    if (!resolve_ref) {
        return get(key, default_value);
    } else {
        resolve_reference(key);
        return get(key, default_value);
    }
}

void Conf::resolve_reference(){
    for(map<string, string>::iterator itr = _options.begin();
            itr != _options.end();
            itr++){
        resolve_reference(itr->first);
    }
}

void Conf::resolve_reference(const string & key) {
   string find_key;
   find_key.reserve(key.length());
   for(uint32_t i = 0; i < key.length(); i++){
       find_key.push_back(tolower(key[i]));
   }
   map< string, string >::iterator itr = _options.find(find_key);
   if(itr != _options.end()){
       string val = itr->second;
       const boost::regex ref_regex = boost::regex("\\{\\{(.*?)\\}\\}",
               boost::regex_constants::icase);
       while(1){
           boost::smatch what;
           bool has_ref = boost::regex_search(val, what, ref_regex);
           if(has_ref){
               string ref_val = what.str(1);
               boost::trim(ref_val);
               if(ref_val != find_key){
                   val = what.prefix() + this->get(ref_val) + what.suffix();
               }
           }else{
               break;
           }
       }
       itr->second = val;
   }
}


vector< string > Conf::get_values(const string & key, bool clean_empty) const {
    string val = get(key);
    vector< string > vals;
    boost::split(vals, val, boost::is_any_of(","));
    for(uint32_t i = 0; i < vals.size(); i++){
        boost::trim(vals[i]);
    }
    if (clean_empty){
        vector<string> res;
        copy_if(vals.begin(), vals.end(), back_inserter(res), [](const string& x){return !x.empty();});
        return res;
    } else {
        return vals;
    }
}

map< string, string > Conf::get_all() const {
    map< string, string > all_options = _options;
    return all_options;
}
