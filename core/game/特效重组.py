# import tools
# import address
# import call
# import logging
#
# g_bufStruct = []
# VectorD64 = []
# g_bufId = 0
#
#
# def FindAllTree(treeObject, vectorD64):
#     global tree_left, old_tree, tree_right
#     tree_head = tools.readLongint(treeObject)
#     tree_left = tools.readLongint(tree_head)
#     while tree_left != tree_head:
#         vectorD64.append(tree_left)
#         tree_right = tools.readLongint(tree_left + 16)
#         if tree_right == 0:
#             logging.error("Debug pointer exception")
#             return False
#         temp = tools.readBytes(tree_right + 25, 1)[0]
#         if temp != 0:
#             tree_right = tools.readLongint(tree_left + 8)
#             temp_1 = tools.readBytes(tree_right + 25, 1)[0]
#             if temp_1 == 0:
#                 temp_2 = tools.readBytes(tree_right + 25, 1)[0]
#                 while 1:
#                     if temp_2 == 0:
#                         data = tools.readLongint(tree_right + 16) != tree_left
#                         if data:
#                             break
#                         tree_left = tree_right
#                         tree_right = tools.readLongint(tree_right + 8)
#                         if tree_right == 0:
#                             logging.error("Debug pointer exception")
#                             return False
#                     else:
#                         break
#             tree_left = tree_right
#             old_tree = tools.readLongint(tree_right)
#             tree_left = tree_right
#             temp_3 = tools.readBytes(old_tree + 25, 1)[0]
#             if temp_3 == 0:
#                 # temp_4 = tools.readBytes(tree_right + 25,1)[0]
#                 while 1:
#                     if tools.readBytes(tree_right + 25, 1)[0] == 0:
#                         tree_right = tools.readLongint(old_tree)
#                         tree_left = old_tree
#                         old_tree = tree_right
#                         if tree_right == 0:
#                             logging.error("Debug pointer exception")
#                             return False
#                     else:
#                         break
#         break
#     result = False
#     for i in vectorD64:
#         if i != 0:
#             result = True
#     return result
#
#
# def allocateMemoryInBytes(len):
#     """
#     按字节分配内存
#     :param len:
#     :return:
#     """
#     递增内存 = 0
#     内存池 = 5365344688
#     寄存池 = 内存池
#     if 寄存池 > 内存池 + 4096 - 512:
#         内存池 = 5365344688 + 1000
#         寄存池 = 内存池
#     if len <= 16:
#         递增内存 = 16
#     if len > 16:
#         递增内存 = int(len / 16) * 16 + 16
#     二次内存 = 寄存池 + 递增内存
#     返回内存 = 寄存池
#     寄存池 = 二次内存
#     return 返回内存
#
#
# def WriteStruct(修该索引, 修改类型, 修改代码, 修改数据):
#     # print(len(g_bufStruct))
#     if 修该索引 > len(g_bufStruct):
#         logging.error("list index out of range")
#         return
#     vector_begin = tools.readLongint(g_bufStruct[修该索引] + 0x38 + 0 * 8)
#     vector_end = tools.readLongint(g_bufStruct[修该索引] + 0x38 + 1 * 8)
#     if vector_end - vector_begin < len(修改数据):
#         Old_Vector = vector_begin
#         vector_begin = allocateMemoryInBytes(len(修改数据))
#         vector_end = vector_begin + len(修改数据)
#         tools.writeInt(g_bufStruct[修该索引] + 0x38 + 0 * 8, vector_begin)
#         tools.writeInt(g_bufStruct[修该索引] + 0x38 + 1 * 8, vector_end)
#         tools.writeInt(g_bufStruct[修该索引] + 0x38 + 2 * 8, vector_end)
#     if 修改代码 != -1:
#         tools.writeInt(g_bufStruct[修该索引] + 0x28, 修改代码)
#         tools.writeInt(g_bufStruct[修该索引] + 0x10, 修改代码)
#         tools.writeInt(g_bufStruct[修该索引] + 0x18, 修改类型)
#     tools.writeBytes(vector_begin, 修改数据)
#     return True
#
#
# def InitBuffStruct(bufStruct):
#     FindAllTree(bufStruct + 0x38, VectorD64)
#     for i in range(len(VectorD64)):
#         g_bufStruct.append(VectorD64[i])
#     return len(g_bufStruct) != 0
#
#
# def IniBuff(id):
#     g_bufStruct.clear()
#     g_bufId = id
#     FindAllTree(tools.readLongint(address.特效基址) + 16, VectorD64)
#     for i in range(len(VectorD64)):
#         data = tools.readInt(VectorD64[i] + 0x20, 4)
#         if data == id:
#             logging.error(f"InitBuffStruct | {InitBuffStruct(VectorD64[i])}")
#             return InitBuffStruct(VectorD64[i])
#     return False
#
#
# def CheckBuff():
#     FindAllTree(tools.readLongint(address.特效基址 + 64), VectorD64)
#     for i in range(len(VectorD64)):
#         print(tools.readInt(tools.readLongint(VectorD64[i] + 0x20), 4))
#         if tools.readInt(tools.readLongint(VectorD64[i] + 0x20), 4) == g_bufId:
#             return True
#     return False
#
#
# def special_effect_call():
#     IniBuff(1249)
#     WriteStruct(1, 0, 12, tools.intTobytes(80, 4))
#     WriteStruct(2, 0, 13, tools.intTobytes(80, 4))
#     WriteStruct(3, 0, 14, tools.intTobytes(80, 4))
#     WriteStruct(4, 1, 4, tools.intTobytes(17, 4))
#     WriteStruct(5, 0, 15, tools.intTobytes(200, 4))
#     WriteStruct(6, 0, 58, tools.intTobytes(-90, 4))
#     WriteStruct(7, 0, 89, tools.intTobytes(200, 4))
#     WriteStruct(8, 0, 96, tools.intTobytes(600000, 4))
#     if CheckBuff() == True:
#         call.tx_close(1249)
#     call.tx_call(1249)
#
#
# # FindAllTree(tools.readLongint(address.特效基址) + 16,VectorD64)
# # call.tx_call(1249)
# special_effect_call()
