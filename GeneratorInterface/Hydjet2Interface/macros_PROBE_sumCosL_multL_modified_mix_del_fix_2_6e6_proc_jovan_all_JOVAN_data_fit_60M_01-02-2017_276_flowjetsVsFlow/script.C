#include <string>
#include <fstream>
#include <streambuf>
#include <iostream>

void script() {
    std::ifstream t("INPUT.txt");
    std::string str((std::istreambuf_iterator<char>(t)),
                     std::istreambuf_iterator<char>());
    cout << str.substr(0, str.size()-1) << endl;
}

