"""
This script contains functions that are decoupled from test cases.
"""


def diff_text(text1: (str, bytes), text2: (str, bytes)):
    max_len = max(len(text1), len(text2))
    for i in range(max_len):
        assert text1[i:i+1] == text2[i:i+1], "The two text is different at index {} :\n< {}\n> {}".format(i, text1[i:i+10], text2[i:i+10])


def diff_dict(dict1, dict2):
    assert len(dict1) == len(dict2)
    for k in dict1.keys():
        assert dict1[k] == dict2[k], "['{}'] is different.".format(k)
