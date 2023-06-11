from core.game.addr import address_all
import call
import logging

from common import helper
from core.game import mem, map_data

g_bufStruct = []
VectorD64 = []
g_bufId = 0


def find_all_tree(tree_object, vector_d64):
    global tree_left, old_tree, tree_right
    tree_head = mem.read_long(tree_object)
    tree_left = mem.read_long(tree_head)
    while tree_left != tree_head:
        vector_d64.append(tree_left)
        tree_right = mem.read_long(tree_left + 16)
        if tree_right == 0:
            logging.error("Debug pointer exception")
            return False
        temp = mem.read_bytes(tree_right + 25, 1)[0]
        if temp != 0:
            tree_right = mem.read_long(tree_left + 8)
            temp_1 = mem.read_bytes(tree_right + 25, 1)[0]
            if temp_1 == 0:
                temp_2 = mem.read_bytes(tree_right + 25, 1)[0]
                while 1:
                    if temp_2 == 0:
                        data = mem.read_long(tree_right + 16) != tree_left
                        if data:
                            break
                        tree_left = tree_right
                        tree_right = mem.read_long(tree_right + 8)
                        if tree_right == 0:
                            logging.error("Debug pointer exception")
                            return False
                    else:
                        break
            tree_left = tree_right
            old_tree = mem.read_long(tree_right)
            tree_left = tree_right
            temp_3 = mem.read_bytes(old_tree + 25, 1)[0]
            if temp_3 == 0:
                # temp_4 = mem.read_bytes(tree_right + 25,1)[0]
                while 1:
                    if mem.read_bytes(tree_right + 25, 1)[0] == 0:
                        tree_right = mem.read_long(old_tree)
                        tree_left = old_tree
                        old_tree = tree_right
                        if tree_right == 0:
                            logging.error("Debug pointer exception")
                            return False
                    else:
                        break
        break
    result = False
    for i in vector_d64:
        if i != 0:
            result = True
    return result


def allocate_memory_in_bytes(len):
    """
    按字节分配内存
    :param len:
    :return:
    """
    递增内存 = 0
    内存池 = 5365344688
    寄存池 = 内存池
    if 寄存池 > 内存池 + 4096 - 512:
        内存池 = 5365344688 + 1000
        寄存池 = 内存池
    if len <= 16:
        递增内存 = 16
    if len > 16:
        递增内存 = int(len / 16) * 16 + 16
    二次内存 = 寄存池 + 递增内存
    返回内存 = 寄存池
    寄存池 = 二次内存
    return 返回内存


def write_struct(修该索引, 修改类型, 修改代码, 修改数据):
    # print(len(g_bufStruct))
    if 修该索引 > len(g_bufStruct):
        logging.error("list index out of range")
        return
    vector_begin = mem.read_long(g_bufStruct[修该索引] + 0x38 + 0 * 8)
    vector_end = mem.read_long(g_bufStruct[修该索引] + 0x38 + 1 * 8)
    if vector_end - vector_begin < len(修改数据):
        vector_begin = allocate_memory_in_bytes(len(修改数据))
        vector_end = vector_begin + len(修改数据)
        mem.write_int()
        mem.write_int(g_bufStruct[修该索引] + 0x38 + 0 * 8, vector_begin)
        mem.write_int(g_bufStruct[修该索引] + 0x38 + 1 * 8, vector_end)
        mem.write_int(g_bufStruct[修该索引] + 0x38 + 2 * 8, vector_end)
    if 修改代码 != -1:
        mem.write_int(g_bufStruct[修该索引] + 0x28, 修改代码)
        mem.write_int(g_bufStruct[修该索引] + 0x10, 修改代码)
        mem.write_int(g_bufStruct[修该索引] + 0x18, 修改类型)
    mem.write_bytes(vector_begin, 修改数据)
    return True


def InitBuffStruct(bufStruct):
    find_all_tree(bufStruct + 0x38, VectorD64)
    for i in range(len(VectorD64)):
        g_bufStruct.append(VectorD64[i])
    return len(g_bufStruct) != 0


def ini_buff(id):
    g_bufStruct.clear()
    find_all_tree(mem.read_long(address_all.特效基址) + 16, VectorD64)
    for i in range(len(VectorD64)):
        data = mem.read_int(VectorD64[i] + 0x20, 4)
        if data == id:
            logging.error(f"InitBuffStruct | {InitBuffStruct(VectorD64[i])}")
            return InitBuffStruct(VectorD64[i])
    return False


def check_buff():
    find_all_tree(mem.read_long(address_all.特效基址 + 64), VectorD64)
    for i in range(len(VectorD64)):
        print(mem.read_int(mem.read_long(VectorD64[i] + 0x20), 4))
        if mem.read_int(mem.read_long(VectorD64[i] + 0x20), 4) == g_bufId:
            return True
    return False


def special_effect_call():
    ini_buff(1249)
    write_struct(1, 0, 12, helper.int_to_bytes(80, 4))
    write_struct(2, 0, 13, helper.int_to_bytes(80, 4))
    write_struct(3, 0, 14, helper.int_to_bytes(80, 4))
    write_struct(4, 1, 4, helper.int_to_bytes(17, 4))
    write_struct(5, 0, 15, helper.int_to_bytes(200, 4))
    write_struct(6, 0, 58, helper.int_to_bytes(-90, 4))
    write_struct(7, 0, 89, helper.int_to_bytes(200, 4))
    write_struct(8, 0, 96, helper.int_to_bytes(600000, 4))
    if check_buff() == True:
        call.tx_close(1249)
    call.tx_call(1249)


# FindAllTree(mem.read_long(address_all.特效基址) + 16,VectorD64)
# call.tx_call(1249)
special_effect_call()
