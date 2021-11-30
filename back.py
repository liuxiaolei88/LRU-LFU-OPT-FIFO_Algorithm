# _*_ coding: utf-8 _*_
"""
Time:     2021/11/25 17:52
Author:   XiaoLei Liu
Version:  V 0.1
File:     os_exp_all.py
"""
import json
from collections import Counter
from flask import Flask
from flask import Response
from flask import request
from flask_cors import cross_origin

app = Flask(__name__)

# memory = [-1, -1, -1]
replace = []  # 记录在序列的哪个地方进行了置换


def opt(item, memory_size):
    memory = []
    for p in range(memory_size):
        memory.append(-1)
    final = ''
    count = 0
    print("使用opt算法")
    for d in range(len(item)):
        replace.append(0)
    pr = 0
    for i in range(len(item)):
        if (i < memory_size):
            memory[i] = item[i]
            count = count + 1
        # 大于内存 可能会出现替换的情况
        else:
            # 看看是否在内存里
            exist = 0
            for j in range(memory_size):
                if item[i] == memory[j]:
                    # 如果已经存在，就不用管
                    exist = 1
                    # print("不缺页")
                    break
            # 如果不存在则需要替换
            if exist == 0:
                later = 0
                need_change = [0, 0, 0]
                for k in item[i + 1:]:
                    for z in range(memory_size):
                        # 就是现在内存里的，序列后面就会用到
                        if k == memory[z]:
                            need_change[z] = 1
                            later = later + 1
                            break
                    if later == memory_size - 1: break
                for y in range(len(memory)):
                    # 需要换
                    if need_change[y] == 0:
                        count = count + 1
                        replace[pr] = memory[y]
                        pr = pr + 1
                        memory[y] = item[i]
                        break

        print(memory, ' ')
        final = final + str(memory)
    return final


def fifo(item, memory_size):
    memory = []
    for p in range(memory_size):
        memory.append(-1)
    final = ''
    pr = 0
    count = 0  # 缺页数记录
    for d in range(len(item)):
        replace.append(0)
    p_memory = 0  # 记录上次换走的是在内存的位置
    print("###使用FIFO 先来先去算法###")
    for i in range(len(item)):
        # 查看是否在内存中
        exist = 0
        for j in range(memory_size):
            if item[i] == memory[j]:
                exist = 1
                break
        #         如果不存在,可能就需要置换
        if exist == 0:
            # 内存没有位置，需要替换
            if memory[p_memory] != -1:
                replace[p_memory] = memory[p_memory]
                pr = pr + 1
            count = count + 1
            # 置换
            memory[p_memory] = item[i]
            p_memory = p_memory + 1
            if p_memory % memory_size == 0:
                p_memory = 0

        print(memory)
        final = final + str(memory)
    return final


def LRU(item, memory_size):
    memory = []
    for p in range(memory_size):
        memory.append(-1)
    final = ''
    print("###使用LRU：如果一个数据在最近一段时间没有被访问到，那么在将来它被访问的可能性也很小###")
    count = 0
    for d in range(len(item)):
        replace.append(0)
    pr = 0
    for i in range(len(item)):
        if (i < memory_size):
            memory[i] = item[i]
            count = count + 1
        # 大于内存 可能会出现替换的情况
        else:
            # 看看是否在内存里
            exist = 0
            for j in range(memory_size):
                if item[i] == memory[j]:
                    # 如果已经存在，就不用管
                    exist = 1
                    # print("不缺页")
                    break
            # 如果不存在则需要替换
            if exist == 0:
                later = 0
                need_change = [0, 0, 0]
                item_temp = item[::-1]
                for k in item_temp[len(item) - i:]:
                    for z in range(memory_size):
                        # 就是现在内存里的，序列后面就会用到
                        if k == memory[z]:
                            need_change[z] = 1
                            later = later + 1
                            break
                    # 只往后找两个
                    if later == memory_size - 1: break
                for y in range(len(memory)):
                    # 需要换
                    if need_change[y] == 0:
                        count = count + 1
                        replace[pr] = memory[y]
                        pr = pr + 1
                        memory[y] = item[i]
                        break

        print(memory, ' ')
        final = final + str(memory)
    return final


def LFU(item, memory_size):
    memory = []
    for p in range(memory_size):
        memory.append(-1)
    final = ''
    pr = 0
    print("###使用LFU算法###")
    count = 0
    for d in range(len(item)):
        replace.append(0)
    pr = 0
    for i in range(len(item)):
        if (i < memory_size):
            memory[i] = item[i]
            count = count + 1
        # 大于内存 可能会出现替换的情况
        else:
            # 看看是否在内存里
            exist = 0
            for j in range(memory_size):
                if item[i] == memory[j]:
                    # 如果已经存在，就不用管
                    exist = 1
                    # print("不缺页")
                    break
            # 如果不存在则需要替换
            if exist == 0:
                later = 0
                need_change = [0, 0, 0]
                # 统计序列中出现的次数
                lru_flag = 0
                f_item = dict(Counter(item[:i]))
                memory_f = {}
                # 找出内存中使用次数，用memory_f 记录
                for u in range(memory_size):
                    memory_f[memory[u]] = (f_item.get(memory[u]))
                # 用sort 给memory_f从小到大排序，最小的就是要换掉的
                memory_f = sorted(memory_f.items(), key=lambda x: x[1], reverse=False)
                # 获取访问次数最小的item
                min_key = next(iter(memory_f))
                # 但如果无没办法选出最小的，那就退化吗？？？？
                # dict(Counter(item[:i-1])).get(2)
                # 如果次数一样多，删除最早的,min_key[0]
                need_replace_index = memory.index(min_key[0])
                replace[need_replace_index] = memory[need_replace_index]
                count = count + 1
                memory[need_replace_index] = item[i]

        print(memory, ' ')
        final = final + str(memory)
    return final


@app.route('/hi', methods=['POST'])
@cross_origin()
def hi():
    student = json.loads(request.get_data(as_text=True))
    print(student)
    print(type(student))
    str = student['x']
    memory_size = int(student['y'])
    options = int(student['z'])
    print("这里是：", str, memory_size, options)
    print("请输入序列:")
    # str = input()
    print("请输入内存大小：")
    print("默认内存大小为3")
    # memory_size = int(input())
    item = []
    for strr in str:
        if strr != ' ':
            item.append(int(strr))
    print("请选择你想要的算法：1：OPT，2：FIFO 先来先去算法,3:LRU,4:LFU")
    # options = int(input())
    if options == 1:
        return opt(item,memory_size)
    if options == 2:
        return fifo(item, memory_size)
    if options == 3:
        return LRU(item, memory_size)
    if options == 4:
        return LFU(item, memory_size)
    return 'yes'


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
    # print("请输入序列:")
    # str = input()
    # print("请输入内存大小：")
    # print("默认内存大小为3")
    # memory_size = int(input())
    # item = []
    # for strr in str:
    #     if strr != ' ':
    #         item.append(int(strr))
    # print("请选择你想要的算法：1：OPT，2：FIFO 先来先去算法,3:LRU,4:LFU")
    # options = int(input())
    # if options == 1:
    #     opt(item)
    # if options == 2:
    #     fifo(item, memory_size)
    # if options == 3:
    #     LRU(item, memory_size)
    # if options == 4:
    #     LFU(item, memory_size)
