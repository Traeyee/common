#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cuiyiwork@foxmail.com
# Created Time: 24/2/2019 3:28 PM


def get_char_index(unicode_char, start_from, ignore_comma):
    char = unicode_char
    if not isinstance(char, unicode):
        char = char.decode("utf-8", "ignore")

    comma_char = 0x2C
    num_char = [0x30, 0x39]
    upeng_char = [0x41, 0x5a]
    loweng_char = [0x61, 0x7a]
    chn_char = [0x4e00, 0x9fa5]

    return_idx = start_from
    unicode_code = ord(char)
    if not ignore_comma:
        if comma_char == unicode_code:
            return start_from
        else:
            return_idx += 1

    if num_char[0] <= unicode_code <= num_char[1]:
        return return_idx + (unicode_code - num_char[0] + 1)
    else:
        return_idx += num_char[1] - num_char[0] + 1

    if upeng_char[0] <= unicode_code <= upeng_char[1]:
        return return_idx + (unicode_code - upeng_char[0] + 1)
    else:
        return_idx += upeng_char[1] - upeng_char[0] + 1

    if loweng_char[0] <= unicode_code <= loweng_char[1]:
        return return_idx + (unicode_code - loweng_char[0] + 1)
    else:
        return_idx += loweng_char[1] - loweng_char[0] + 1

    if chn_char[0] <= unicode_code <= chn_char[1]:
        return return_idx + (unicode_code - chn_char[0] + 1)
    else:
        return_idx += chn_char[1] - chn_char[0] + 1

    return -1


def get_filtered_unicode_str(unc_str, start_from=0, ignore_comma=False):
    str1 = unc_str
    if not isinstance(str1, unicode):
        str1 = str1.decode("utf-8", "ignore")
    return_str = u""
    for char in str1:
        idx = get_char_index(char, start_from=start_from, ignore_comma=ignore_comma)
        if -1 != idx:
            return_str += char

    return return_str


def main():
    str1 = "Unicode 编码包含了不同写法的字，如“ɑ/a”、“户/户/戸”。"
    str2 = get_filtered_unicode_str(str1)
    print(str2)


if __name__ == '__main__':
    main()
