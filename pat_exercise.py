# -*- coding:utf-8 -*-
'''
给定的任一不超过1000的正整数n，简单地数一下，需要多少步（砍几下）才能得到n=1
'''
# num = int(raw_input())
def count_step(num):
    step = 0
    if num > 1000:
        print 'beyond 1000?'
    while num > 1:
        if num % 2 == 0:
            num = num / 2
            step += 1
        elif num % 2 == 1:
            num = (num * 3 + 1) / 2
            step += 1
    return step

'''
读入一个自然数n，计算其各位数字之和，用汉语拼音写出和的每一位数字
'''

def calc_sum(num):
    num_str = str(num)
    num_sum = 0
    re_list = []
    for i in num_str:
        num_sum += int(i)
    num_sum_str = str(num_sum)
    num_dict = {1:"yi", 2:"er", 3:"san", 4:"si", 5:"wu", 6:"liu", 7:"qi", 8:"ba", 9:"jiu", 0:"ling"}
    for j in num_sum_str:
        re_list.append(num_dict[int(j)])
    result = ' '.join(i for i in re_list)
    return  result
'''
单身狗
'''
def singe_dog():
    num = int(raw_input())
    couple_list = []
    person_list = []
    count = 0
    while num > 0:
        couple_id = raw_input()
        if ' ' in couple_id:
            count += 1
            if count == 1:
                coupe_li = couple_id.split()
                if len(str(coupe_li[0])) == 5 and len(str(coupe_li[1])) == 5:
                    couple_list.append(couple_id)
                else:
                    print 'wrong character'
                count = 0
            else:
                print 'wrong input'
        else:
            print 'need black space'
        num -= 1
    couple_fin = []
    for i in couple_list:
        temp = i.split()
        couple_fin.append(temp)
    party_num = int(raw_input())
    person_id = raw_input()
    person_list = person_id.split()
    if len(person_list) == party_num:
        for cp in couple_fin:
            if cp[0] in person_list and cp[1] in person_list:
                party_num -= 2
                person_list.remove(cp[0])
                person_list.remove(cp[1])
    else:
        print 'party_person is too few'
    person_list = sorted(person_list)
    person_str = ' '.join(i for i in person_list)
    print party_num
    return person_str

'''
读入n名学生的姓名、学号、成绩，分别输出成绩最高和成绩最低学生的姓名和学号
其中，没有两个学生的成绩是相同的
'''
def score_rank():
    num = int(raw_input())
    score_str = []
    score_list = []
    dict_score = {}
    while num > 0:
        score = raw_input()
        score_str.append(score)
        num -= 1
    for i in score_str:
        temp = i.split()
        score_list.append(temp)
    for i in score_list:
        temp2 = ' '.join(j for j in i[:2])
        dict_score[i[2]] = temp2
    # result = sorted(dict_score.items(), key=lambda item:item[0])
    result = sorted(dict_score.keys())
    return dict_score[result[-1]], dict_score[result[0]]

def calc_s():
    num1 = int(raw_input())
    num2 = int(raw_input())
    if num1 >= -1000000 and num2 <= 1000000:
        sum_num = num1 + num2
        if sum_num > 0:
            sum1 = sum_num / 1000
            sum2 = sum_num % 1000
            result = str(sum1) + ',' + str(sum2)
        elif sum_num < 0:
            sum_num = -1 * sum_num
            sum1 = sum_num / 1000
            sum2 = sum_num % 1000
            result = str(-sum1) + ',' + str(sum2)
    else:
        print 'wrong input'
    return result


