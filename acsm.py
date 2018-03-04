#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
    Aho-Corasick String Match.
    A python implementation of aho-corasick string searching algorithm.

    Usage:
        import acsm
        string_match = acsm.StringMatch()
        pattern_list = ["java", "c", "c++", "python"]
        string_match.read_from_iterable(pattern_list)
        print(string_match.match("Python is awesome", True))
'''

class ACSMNode(object):
    __slots__ = ['child_map', 'fail_node', 'pattern_index']
    def __init__(self):
        self.child_map = {}
        self.fail_node = None
        self.pattern_index = -1

class StringMatch:
    '''
    AC多模匹配
    '''
    def __init__(self):
        self._root = ACSMNode()
        self._words_list = []
        self._is_build = False

    def read_from_file(self, file_path):
        '''
        通过文件初始化
        一行一个pattern
        '''
        try:
            f_in = open(file_path, "r")
            for count, line in enumerate(f_in):
                line = line.strip()
                if not self._insert(line, count):
                    f_in.close()
                    raise
                self._words_list.append(line)
            f_in.close()
            self._build()
            return True
        except:
            return False

    def read_from_iterable(self, iterable_obj):
        '''
        通过迭代器进行初始化
        '''
        try:
            for count, line in enumerate(iterable_obj):
                if not self._insert(line, count):
                    raise
                self._words_list.append(line)
            self._build()
            return True
        except Exception as e:
            print(e)
            return False

    def match(self, query, ignore_cover=False):
        '''
        进行匹配
        ignore_cover : 是否忽略覆盖的情况
        '''
        if not self._is_build:
            return None
        match_result = []
        curr_node = self._root
        for pos in range(len(query)):
            char = query[pos]
            while char not in curr_node.child_map and curr_node != self._root:
                curr_node = curr_node.fail_node
            if char not in curr_node.child_map:
                continue
            curr_node = curr_node.child_map[char]
            tmp = curr_node
            while tmp != self._root:
                if tmp.pattern_index != -1:
                    word = self._words_list[tmp.pattern_index]
                    match_result.append((word, pos-len(word)+1))
                tmp = tmp.fail_node

        if len(match_result) < 2 or not ignore_cover:
            return match_result

        ## ignore cover
        match_result = sorted(match_result, key=lambda a : a[1])
        end_pos = [i[1] + len(i[0]) for i in match_result]
        ignore_result = []
        ok_idx = 0
        for i in range(1, len(match_result)):
            ## 后面覆盖前面
            if match_result[ok_idx][1] >= match_result[i][1] and end_pos[ok_idx] <= end_pos[i]:
                ok_idx = i
            ## 前面覆盖后面
            elif match_result[ok_idx][1] <= match_result[i][1] and end_pos[ok_idx] >= end_pos[i]:
                pass
            ## 下一个pattern和当前已经没有互相覆盖的可能
            else:
                ignore_result.append(match_result[ok_idx])
                ok_idx = i
        ## 最后补充输出最后一个ok的pattern
        ignore_result.append(match_result[ok_idx])
        return ignore_result

    def _insert_by_iter(self, iterable):
        pass

    def _insert(self, word, word_count):
        '''
        插入节点
        '''
        if self._is_build == True or len(word) < 1:
            return false

        curr_node = self._root
        for char in word:
            if char not in curr_node.child_map:
                curr_node.child_map[char] = ACSMNode()
            curr_node = curr_node.child_map[char]
        curr_node.pattern_index = word_count
        return True

    def _build(self):
        '''
        建立失配指针
        '''
        node_list = [self._root]
        node_index = 0
        while node_index < len(node_list):
            curr_parent_node = node_list[node_index]
            for char in curr_parent_node.child_map:
                child_node = curr_parent_node.child_map[char]
                child_node.fail_node = self._root
                curr_fail_node = curr_parent_node.fail_node
                while curr_fail_node != None:
                    if char in curr_fail_node.child_map:
                        child_node.fail_node = curr_fail_node.child_map[char]
                        break
                    else:
                        curr_fail_node = curr_fail_node.fail_node
                node_list.append(curr_parent_node.child_map[char])
            node_index += 1

        self._is_build = True

