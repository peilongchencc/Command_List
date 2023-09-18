# 全角转半角
def _str_qj_2_bj(text):
    rstring = ""
    for uchar in text:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring
tmp_text = _str_qj_2_bj(text)


def _str_qj_2_bj(text):
    return ''.join([chr(ord(uchar) - 65248) if 65281 <= ord(uchar) <= 65374 else chr(32) if ord(uchar) == 12288 else uchar for uchar in text])

tmp_text = _str_qj_2_bj(text)


def clean(text:str) -> str:
    tmp_text = _str_qj_2_bj(text)
    tmp_char_list = _remove_stop_chars(tmp_text)

    if 0 == len(tmp_char_list):
        return ''

    _reduce_redup_chars(tmp_char_list)

    if '.' in tmp_char_list:
        _try_to_convert_dot_to_quanjiao(tmp_char_list)

    if '十' in tmp_char_list:
        _try_to_convert_shi_to_plus(tmp_char_list)

    if '啥' in tmp_char_list:
        _replace_sha_to_shenme(tmp_char_list)

    tmp_text = ''.join(tmp_char_list)
    if '#' in tmp_text:
        tmp_text = tmp_text.replace('#', '')

    if '×' in tmp_text:
        tmp_text = tmp_text.replace('×', 'x')
    
    tmp_end_index = len(tmp_text) - 1
    if tmp_end_index >= 0 and tmp_text[tmp_end_index] in _Pu_At_Sentence_Tail:
        tmp_text = tmp_text[0:tmp_end_index]
    
    if _Emoji.search(tmp_text):
        tmp_text = _Emoji.sub('', tmp_text)

    return tmp_text