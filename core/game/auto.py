"""
自动刷图主线程
"""
import _thread
import random
import sys
import time
import traceback

from common import config
from common import helper, logger
from core.game import mem, skill, run_time, person_base, map_base
from core.game import call, init, address


class Auto:
    # 首次进图
    firstEnterMap = False
    addBuff = False
    # 已完成刷图次数
    completedNum = 0
    # 线程开关
    thread_switch = False
    # 线程句柄
    threadHande = None
    # 任务对象
    task = None

    traversal = None

    map_data = None

    pack = None

    pick = None

    equip = None

    game_map = None

    skill = None

    @classmethod
    def __init__(cls, task, traversal, map_data, pack, pick, equip, game_map):
        cls.task = task
        cls.traversal = traversal
        cls.map_data = map_data
        cls.pack = pack
        cls.pick = pick
        cls.equip = equip
        cls.game_map = game_map

    @classmethod
    def test_func(cls):
        while init.global_data.manual_switch:
            code = skill.skill_map_cool_down_all()
            helper.key_press_release(code)
            logger.info("测试结果 {}".format(code), 1)
            time.sleep(0.1)

    @classmethod
    def hide_body(cls):
        init.global_data.manual_switch = not init.global_data.manual_switch
        call.hide_call(call.person_ptr())

    @classmethod
    def skill_nothing(cls):
        if cls.map_data.get_stat() == 3:
            # 透明call
            logger.info("技能三无 {}", 2)
            call.skill_nothing()

    @classmethod
    def follow_monster_switch(cls):
        # 跟随怪物
        if config().getint("自动配置", "跟随打怪") == 1:
            while True:
                if init.map_data.is_open_door():
                    return
                cls.traversal.follow_monster()

    @classmethod
    def pick_item(cls):
        # 捡物品
        cls.pick.pickup()

    @classmethod
    def switch(cls):
        """自动开关"""
        init.global_data.auto_switch = not init.global_data.auto_switch
        cls.thread_switch = init.global_data.auto_switch
        if cls.thread_switch:
            cls.threadHande = _thread.start_new_thread(cls.auto_thread, ())
            logger.info("自动刷图 [ √ ]", 1)
        else:
            init.global_data.auto_switch = False
            cls.thread_switch = False
            logger.info("自动刷图 [ x ]", 1)

    @classmethod
    def auto_thread(cls):
        """自动线程"""
        while cls.thread_switch:
            try:
                time.sleep(0.3)
                if cls.map_data.is_dialog_esc():
                    helper.key_press_release('esc')
                    helper.key_press_release('space')
                    continue
                if cls.map_data.is_dialog_esc() and (cls.map_data.is_dialog_a() and cls.map_data.is_dialog_b()):
                    helper.key_press_release('esc')
                    helper.key_press_release('space')
                    continue

                # 进入城镇
                if cls.map_data.get_stat() == 0:
                    time.sleep(0.2)
                    cls.enter_town()
                    continue

                # 城镇处理
                if cls.map_data.get_stat() == 1 and cls.map_data.is_town() is True:
                    cls.town_handle()
                    continue

                # 进入副本
                if cls.map_data.get_stat() == 2:
                    if init.global_data.map_id_list.__len__() != 0:
                        # 有列表先用列表
                        temp_map_id = init.global_data.map_id_list.pop()
                        temp_level = init.global_data.map_list_level
                        cls.enter_map(temp_map_id, temp_level)
                        continue
                    cls.enter_map(init.global_data.map_id, init.global_data.map_level)
                    continue

                # 在地图内
                if cls.map_data.get_stat() == 3:
                    while cls.map_data.get_stat() == 3 and cls.thread_switch and not cls.map_data.is_pass():
                        # 第一个房间 加buff
                        if cls.firstEnterMap is False and cls.map_data.is_town() is False:
                            hide = config().getint("自动配置", "开启透明")
                            if hide == 1:
                                # 透明call
                                call.hide_call(call.person_ptr())
                            # sss评分
                            score = config().get("自动配置", "评分")
                            mem.write_long(mem.read_long(address.PFAddr) + address.CEPfAddr, int(score))
                            # 无视建筑
                            # cls.traversal.ignore_building(True)
                            # 进图开启功能
                            # cls.start_func()
                            cls.firstEnterMap = True
                        if cls.firstEnterMap is True and cls.addBuff is False:
                            buff = config().get("自动配置", "buff技能")
                            buff_list = buff.split(",")
                            skill.check_skill_down_single_while(buff_list)
                            cls.addBuff = True

                        # 跟随怪物
                        if config().getint("自动配置", "跟随打怪") > 0:
                            cls.traversal.follow_monster()

                        start_time = time.time()
                        # 过图
                        if cls.map_data.is_open_door() is True and cls.map_data.is_boss_room() is False:
                            # 捡物品
                            cls.pick.pickup()
                            time.sleep(random.uniform(0.1, 0.5))
                            # 过图
                            cls.pass_map()
                            logger.info("过图耗时 {}".format(time.time() - start_time), 1)
                            continue
                    # 通关
                    if cls.map_data.is_boss_room():
                        if cls.map_data.is_pass():
                            # 捡物品
                            cls.pick.pickup()
                            # 关闭功能
                            cls.start_func()
                            # 关闭穿透
                            # cls.traversal.ignore_building(False)
                            # 退出副本
                            cls.quit_map()
                            cls.firstEnterMap = False
                            cls.addBuff = False
            except Exception as err:
                print("-----------自动线程开始-----------")
                except_type, _, except_traceback = sys.exc_info()
                print(except_type)
                print(err.args)
                print(except_traceback)
                print('-----------')
                for i in traceback.extract_tb(except_traceback):
                    print(i)
                print("-----------自动线程结束-----------")

    @classmethod
    def start_func(cls):
        func_mod = config().getint("自动配置", "开启功能")
        if func_mod == 1:
            print("功能1为实现")
        if func_mod == 2:
            print("功能2为实现")
        if func_mod == 3:
            print("功能3为实现")

    @classmethod
    def enter_town(cls):
        """进入城镇"""
        role_num = config().getint("自动配置", "角色数量")
        init.global_data.completed_role = init.global_data.completed_role + 1
        if init.global_data.completed_role > role_num:
            logger.info("指定角色完成所有角色", 2)
            logger.info("自动刷图 [ x ]", 2)
            cls.thread_switch = False
            init.global_data.auto_switch = False
            return

        time.sleep(0.2)
        cls.pack.select_role(init.global_data.completed_role)
        # 选择角色后初始化动作
        cls.select_role_pre()

        time.sleep(0.5)
        logger.info("进入角色 {} ".format(init.global_data.completed_role), 2)
        logger.info("开始第 {} 个角色,剩余疲劳 {}".format(init.global_data.completed_role + 1, cls.map_data.get_pl()),
                    2)
        while cls.thread_switch:
            time.sleep(0.2)
            # 进入城镇跳出循环
            if cls.map_data.get_stat() == 1:
                break

    @classmethod
    def town_handle(cls):
        """城镇处理"""
        check_fatigue = config().getint("自动配置", "预留疲劳")
        if cls.map_data.get_pl() <= check_fatigue:
            cls.return_role()
            return

        time.sleep(0.5)
        # 分解装备
        cls.equip.handle_equip()

        # 随机处理
        breaks = config().getint("自动配置", "休息次数")
        remainder = run_time.modulo_algorithm(cls.completedNum, breaks)
        if remainder == 0:
            change = config().getint("自动配置", "休息切角")
            cls.completedNum += 1
            if change == 1:
                # 切换角色
                cls.return_role()
                return

        # 1 剧情 2 搬砖
        auto_model = config().getint("自动配置", "自动模式")
        first_upgrade = config().getint("自动配置", "优先升级")
        map_select = config().getint("自动配置", "手动选择")
        normal_map = list(map(int, config().get("自动配置", "普通地图").split(",")))
        super_map = list(map(int, config().get("自动配置", "英豪地图").split(",")))

        if auto_model == 1:
            cls.get_map_data()
        elif auto_model == 2:
            if cls.map_data.get_role_level() < 110:
                if first_upgrade == 1:
                    cls.get_map_data()
            else:
                map_ids = []
                if map_select == 0:
                    init.global_data.map_level = cls.fame_level()
                    # 自动模式
                    if person_base.get_fame() < 23330 and map_select == 0:
                        map_ids = normal_map
                    else:
                        map_ids = super_map
                elif map_select == 1:
                    # 普通地图
                    map_ids = normal_map
                elif map_select == 2:
                    # 英豪地图
                    map_ids = super_map

                if map_ids.__len__() > 0:
                    random_number = random.randint(0, len(map_ids) - 1)
                    init.global_data.map_id = map_ids[random_number]
        elif auto_model == 3:
            # 每日地图
            if init.global_data.daily_map.__len__() > 0:
                init.global_data.map_id = init.global_data.daily_map.pop()
            else:
                change = config().getint("自动配置", "休息切角")
                if change == 1:
                    # 切换角色
                    cls.return_role()
                    return

        if init.global_data.map_id == 0:
            logger.info("地图编号为空,无法切换区域", 2)
            exit(0)

        time.sleep(0.2)
        # 区域发包
        call.area_call(init.global_data.map_id)

        time.sleep(0.2)
        cls.select_map()

    @classmethod
    def get_map_data(cls):
        temp_map = cls.task.handle_main()
        if type(temp_map) == list:
            init.global_data.map_id = temp_map[0]
            if init.global_data.map_id_list.__len__() > 0:
                return
            init.global_data.map_id_list = temp_map
        else:
            init.global_data.map_id = temp_map
            init.global_data.map_level = 0

    @classmethod
    def select_map(cls):
        """选图"""
        while cls.thread_switch:
            time.sleep(0.2)
            # 选图
            cls.pack.select_map()
            # 不在选图界面跳出循环
            if cls.map_data.get_stat() == 2:
                break

    @classmethod
    def return_role(cls):
        """返回角色"""
        logger.info("疲劳值不足 · 即将切换角色", 2)
        time.sleep(0.2)
        # 返回选择角色清除数据动作
        cls.pack.return_role()
        while cls.thread_switch:
            time.sleep(0.2)
            if cls.map_data.get_stat() == 0:
                break

    @classmethod
    def enter_map(cls, map_id: int, map_level: int):
        """进图  这个5 会自动适配是否进图的  从高到低 没开图 自动开图 """
        auto_down = config().getint("自动配置", "地图难度")
        auto_type = config().getint("自动配置", "自动模式")
        while cls.map_data.get_stat() == 2 and cls.thread_switch:
            for i in range(4, -1, -1):
                if cls.map_data.get_stat() == 3:
                    break
                if cls.map_data.get_stat() == 2:
                    cls.pack.go_map(map_id, i, 0, 0)
                    time.sleep(1)
                if cls.map_data.get_stat() == 1:
                    cls.select_map()

    @classmethod
    def pass_map(cls):
        """过图"""
        if cls.map_data.is_open_door() is False or cls.map_data.is_boss_room() is True:
            return

        over_map = config().getint("自动配置", "过图方式")
        over_map_size = config().getint("自动配置", "卡门重试")
        random_wait = config().getint("自动配置", "过图等待")

        '''过图随机'''
        if random_wait != 0:
            time.sleep(random.uniform(0, random_wait))

        if over_map > 0:
            # 寻路过图 获取地图数据
            map_data = cls.game_map.map_data()
            if len(map_data.map_route) >= 2:
                direction = cls.game_map.get_direction(map_data.map_route[0], map_data.map_route[1])
                if over_map == 1:
                    call.over_map_call(direction)
                if over_map == 2:
                    while cls.map_data.is_open_door() is True:
                        call.drift_over_map(direction)
                        time.sleep(random.uniform(0.2, 0.5))
                    if cls.map_data.is_open_door() is True and cls.map_data.is_boss_room() is False:
                        logger.info("被卡门 强制过图", 1)
                        call.over_map_call(direction)

    @classmethod
    def cross_fissure(cls):
        map_obj = init.map_data
        if map_obj.get_stat() != 3:
            return

        rw_addr = call.person_ptr()
        map_data = mem.read_long(mem.read_long(rw_addr + address.DtPyAddr) + 16)
        start = mem.read_long(map_data + address.DtKs2)
        end = mem.read_long(map_data + address.DtJs2)
        obj_num = int((end - start) / 24)
        for obj_tmp in range(obj_num):
            obj_ptr = mem.read_long(start + obj_tmp * 24)
            obj_ptr = mem.read_long(obj_ptr + 16) - 32
            if obj_ptr > 0:
                obj_type_a = mem.read_int(obj_ptr + address.LxPyAddr)
                if obj_type_a == 529 or obj_type_a == 545 or obj_type_a == 273 or obj_type_a == 61440:
                    obj_camp = mem.read_int(obj_ptr + address.ZyPyAddr)
                    obj_code = mem.read_int(obj_ptr + address.DmPyAddr)
                    obj_blood = mem.read_long(obj_ptr + address.GwXlAddr)
                    if obj_camp > 0 and obj_ptr != rw_addr:
                        monster = map_obj.read_coordinate(obj_ptr)
                        if obj_blood > 0:
                            call.drift_call(rw_addr, monster.x, monster.y, 0, 2)

    @classmethod
    def quit_map(cls):
        """出图"""
        cls.completedNum = cls.completedNum + 1
        logger.info("自动刷图 [ {} ] 剩余疲劳 [ {} ]".format(cls.completedNum, cls.map_data.get_pl()), 2)
        time.sleep(0.2)
        # 翻牌
        cls.pack.get_income(0, random.randint(0, 3))

        out_type = config().getint("自动配置", "出图方式")
        if out_type == 2:
            out_value = config().get("自动配置", "出图按键")
            while cls.map_data.get_stat() == 3 or not cls.map_data.is_town():
                time.sleep(0.5)
                helper.key_press_release(out_value)

        if out_type == 0:
            time.sleep(5)

        cls.level_map_while()

    @classmethod
    def level_map_while(cls):
        while cls.thread_switch:
            time.sleep(0.2)
            # 出图
            cls.pack.leave_map()
            if cls.map_data.get_stat() == 1 or cls.map_data.is_town():
                break

    # 英豪名望判断等级
    @classmethod
    def fame_level(cls):
        fame = person_base.get_fame()
        if fame < 25837:
            return 0
        if fame < 29369:
            return 1
        if fame < 30946:
            return 2
        if fame < 32523:
            return 3
        return 4

    @classmethod
    def select_role_pre(cls):
        # 角色技能
        init.skill_data = {}
        # 角色名称
        role_name = person_base.get_role_name()
        logger.info("进入角色 {} ".format(role_name), 2)
        daily_map = list(map(str, config().get("自动配置", "每日地图").split(",")))
        daily_first = int(config().get("自动配置", "优先每日"))
        init.global_data.daily_map = []
        if daily_first == 1:
            for map_temp in daily_map:
                code = map_base.data.get(map_temp)
                init.global_data.daily_map.append(code)
