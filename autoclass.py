# coding=utf-8
import pyautogui
import win32gui
import pyperclip
import time

LESSON_NAME = 0
WEEK_DAY = 1
BEGIN_H = 2
BEGIN_M = 3
END_H = 4
END_M = 5


class FuckInfo:
    def __init__(self):
        self.__infos__ = []

    def Extract(self, file_path):
        try:
            file = open(file_path, 'r', encoding='utf-8')
            lines = file.readlines()
            self.__infos__.clear()
            for line in lines:
                info_seg = line.split()
                print(info_seg)
                self.__infos__.append([info_seg[LESSON_NAME], int(info_seg[WEEK_DAY]), int(info_seg[BEGIN_H]),
                                  int(info_seg[BEGIN_M]), int(info_seg[END_H]), int(info_seg[END_M])])
            return True
        except FileNotFoundError:
            print("file don't exit")
            return False
        except ValueError:
            print("file format error")
            return False
        except IndexError:
            print("info out of index")

    def GetTimeDistance(self):
        m = 0
        min_m = 999
        lesson_name = ''
        moment_type = 'NOLESSON'
        now_time = time.localtime()
        for info in self.__infos__:
            if info[WEEK_DAY] == now_time.tm_wday:
                m = abs(60 * info[BEGIN_H] + info[BEGIN_M] - 60 * now_time.tm_hour - now_time.tm_min)
                if m < min_m:
                    min_m = m
                    lesson_name = info[LESSON_NAME]
                    moment_type = 'BEGIN'
                m = abs(60 * info[END_H] + info[END_M] - 60 * now_time.tm_hour - now_time.tm_min)
                if m < min_m:
                    min_m = m
                    lesson_name = info[LESSON_NAME]
                    moment_type = 'END'
        return [moment_type, lesson_name, min_m]


class FuckDingDing:
    def __init__(self, search_pos, paste_pos, search_result_pos, lesson_enter_pos, lesson_exit_pos):
        self.__hwnd__ = 0
        self.__search_pos__ = search_pos
        self.__search_result_pos__ = search_result_pos
        self.__paste_pos__ = paste_pos
        self.__lesson_enter_pos__ = lesson_enter_pos
        self.__lesson_exit_pos__ = lesson_exit_pos

    def DisplayWindow(self):
        self.__hwnd__ = win32gui.FindWindow(None, "钉钉")
        if self.__hwnd__ == 0:
            return False
        win32gui.ShowWindow(self.__hwnd__, 3)
        win32gui.SetForegroundWindow(self.__hwnd__)
        return True

    def ChangeGroup(self, search_info):
        pyautogui.click(self.__search_pos__[0], self.__search_pos__[1])
        pyperclip.copy(search_info)
        pyautogui.rightClick()
        pyautogui.click(self.__paste_pos__[0], self.__paste_pos__[1])
        time.sleep(1)  # 等待加载
        pyautogui.click(self.__search_result_pos__[0], self.__search_result_pos__[1])

    def EnterLesson(self):
        pyautogui.click(self.__lesson_enter_pos__[0], self.__lesson_enter_pos__[1])
        return self.__hwnd__ != win32gui.GetForegroundWindow()

    def ExitLesson(self):
        pyautogui.click(self.__lesson_exit_pos__[0], self.__lesson_exit_pos__[1])
        return self.__hwnd__ == win32gui.GetForegroundWindow()


flag = 0
fuckdingding = FuckDingDing([192, 90], [220, 260], [220, 260], [700, 130], [0, 0])
fuckinfo = FuckInfo()
fuckinfo.Extract('info.txt')
while True:
    time.sleep(60)
    timedistance = fuckinfo.GetTimeDistance()
    if timedistance[2] < 10:
        if timedistance[0] == 'BEGIN':
            if flag != 3:
                flag = 1  # 正在进入
        elif timedistance[0] == 'END':
            if flag == 3:  # 正在上课
                flag = 2  # 正在退出
    if flag == 1:  # 正在进入
        if fuckdingding.DisplayWindow():
            if fuckdingding.EnterLesson():
                flag = 3
    if flag == 2:  # 正在退出
        if fuckdingding.ExitLesson():
            flag = 0
