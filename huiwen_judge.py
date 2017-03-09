# -*- coding:utf-8 -*-
'''
判断两个字符串是否为回文字符串
例如，'heart' 和 'earth'，'python' 和 'typhon' 
'''
def word_count(str_):
    dict_ = {}
    for i in str_:
        if i not in dict_:
            dict_[i] = 1
        else:
            dict_[i] += 1
    return dict_

def judge_huiwen(s1, s2):
    dict1 = word_count(s1)
    dict2 = word_count(s2)
    if dict1 == dict2:
        print 'they are match'
    else:
        print 'not match'

judge_huiwen('abbcce','bacebc')
