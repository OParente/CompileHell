// resource_lib.hpp
#pragma once
#include <string>
#include <map>
#include <fstream>
#include <sstream>
#include <vector>

namespace ResourceLib {

const int SECRET_KEY = 0x9989;
const std::string HEADER = "# RESXX FILE v2\n";

// XOR encrypt/decrypt
inline std::string xor_crypt(const std::string& text) {
    std::string out = text;
    for (char& c : out) c ^= SECRET_KEY;
    return out;
}

// Base64 (minimal implementation)
static const std::string base64_chars =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

inline std::string base64_encode(const std::string& in) {
    std::string out;
    int val = 0, valb = -6;
    for (unsigned char c : in) {
        val = (val << 8) + c;
        valb += 8;
        while (valb >= 0) {
            out.push_back(base64_chars[(val >> valb) & 0x3F]);
            valb -= 6;
        }
    }
    if (valb > -6) out.push_back(base64_chars[((val << 8) >> (valb + 8)) & 0x3F]);
    while (out.size() % 4) out.push_back('=');
    return out;
}

inline std::string base64_decode(const std::string& in) {
    std::vector<int> T(256, -1);
    for (int i = 0; i < 64; i++) T[base64_chars[i]] = i;
    std::string out;
    int val = 0, valb = -8;
    for (unsigned char c : in) {
        if (T[c] == -1) break;
        val = (val << 6) + T[c];
        valb += 6;
        if (valb >= 0) {
            out.push_back(char((val >> valb) & 0xFF));
            valb -= 8;
        }
    }
    return out;
}

// Encode a line
inline std::string encode_line(const std::string& line) {
    return base64_encode(xor_crypt(line));
}

// Decode a line
inline std::string decode_line(const std::string& line) {
    return xor_crypt(base64_decode(line));
}

// Save .resxx file
inline void save_resxx(const std::string& path, const std::map<std::string, std::map<std::string, std::string>>& data) {
    std::ofstream f(path);
    f << HEADER;
    for (const auto& [section, items] : data) {
        f << encode_line("Section: " + section) << "\n";
        for (const auto& [k, v] : items) {
            f << encode_line(k + "=" + v) << "\n";
        }
    }
    f.close();
}

// Load .resxx file
inline std::map<std::string, std::map<std::string, std::string>> load_resxx(const std::string& path) {
    std::map<std::string, std::map<std::string, std::string>> data;
    std::ifstream f(path);
    std::string line, section;
    while (std::getline(f, line)) {
        if (line.empty() || line[0] == '#') continue;
        std::string decoded = decode_line(line);
        if (decoded.find("Section: ") == 0) {
            section = decoded.substr(9);
            data[section] = {};
        } else if (!section.empty() && decoded.find('=') != std::string::npos) {
            auto pos = decoded.find('=');
            std::string k = decoded.substr(0, pos);
            std::string v = decoded.substr(pos + 1);
            data[section][k] = v;
        }
    }
    return data;
}

}