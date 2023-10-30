import argparse as aps
import os
import time

import cmd2 as cmd
import constant
from cmd2 import with_argparser

__all__ = [constant]

from Command.DeleteCommand import DeleteCommand
from Command.DirTreeCommand import DirTreeCommand
from Command.InsertCommand import InsertCommand
from Command.ListCommand import ListCommand
from Command.ListTreeCommand import ListTreeCommand
from Command.LoadCommand import LoadCommand
from Command.SaveCommand import SaveCommand
from Command.UndoCommand import UndoCommand

current_load_file = ""  # initialize global variable a，为空表示当前未加载文件
command_stack = []  # 保存可以被undo的编辑指令
input_history = []  # 保存用户的输入记录
constant.WORKPATH = "./data"
session_time = vars
start_times = dict()
constant.WORKPATH = "./data"
constant.TEMP_FILE = "temp_file.md"
constant.LOG_DIR = "./log.md"


def check_opt_num(opt, num):
    """
    check opt_num >= num
    """

    if num <= 0:
        return True
    # 以下，至少要有一个参数
    if len(opt) == 0 or opt.isspace():
        print("prompt: no opt, you need at least " + str(num) + " opts")
        return False
    opt_num = 0
    for _ in opt.split(' '):
        opt_num += 1
    if opt_num < num:
        print("prompt: " + str(opt_num) + " opts, you need at least " + str(num) + " opts")
        return False
    return True


#
def check_has_load():
    """"
    check a file has been loaded
    """
    if len(current_load_file) == 0:
        print("prompt: you need to load a file firstly.")
        return False
    return True


def cal_time(second):
    times = []
    end = ' '
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    times.append(day)
    times.append(hour)
    times.append(minute)
    times.append(second)
    name = ['天', '小时', '分钟', '秒']
    for i in range(0, len(times)):
        if times[i] != 0:
            end += str(times[i]) + str(name[i])
    return end


class NewInput(cmd.Cmd):
    redo_command = None

    def __init__(self):
        super().__init__()

    '''
    # 使用 cmd2 处理参数，解析命令词后的 opt 字符串，较为灵活

    def do_checkopt(self, opt):
        if len(opt)==0 or opt.isspace():
            print("no opt")
        else:
            opts = [int(i) for i in opt.split(' ')]
            print(opts)

    # 使用 cmd2 + argparse 配置命令行参数, eg. plus 1 2

    argparse_plus=aps.ArgumentParser()
    argparse_plus.add_argument('num1',type=int,help='arg1_help')
    argparse_plus.add_argument('num2',type=int,help='arg1_help')
    @with_argparser(argparse_plus)
    def do_plus(self,opt):
        print(opt.num1 + opt.num2)

    # 注：使用 argparse 隐含参数检查，否则可以调用 check_opt_num(opt,num) 检查参数个数至少为 num
    '''

    @staticmethod
    def do_exit(_):
        """
        exit
        退出文件
        """
        print("Exiting the program...")
        return True

    # load 文件路径
    argparse_load = aps.ArgumentParser()
    argparse_load.add_argument('file_path', type=str, help='path of file')

    @with_argparser(argparse_load)
    def do_load(self, opt):
        input_history.append('load' + opt.file_path)
        # 参数检查: argparse 隐含
        # 构建命令，加入 command_stack 并执行
        command = LoadCommand(opt.file_path)
        command_stack.clear()
        if command.execute():
            # 加载成功, 改变命令行提示词
            global current_load_file
            current_load_file = opt.file_path
            self.prompt = "<" + opt.file_path + "> "
            start_times[current_load_file]=int(time.time())#记录开始时间时间

    def do_save(self, opt):
        """
        save
        保存文件
        """
        input_history.append('save' + opt)
        global current_load_file
        if not check_has_load():
            return
        save_command = SaveCommand(current_load_file)
        command_stack.clear()
        save_command.execute()

        current_load_file = ""
        # 改变命令行提示词
        self.prompt = "<Editor> "

    @staticmethod
    def do_list(opt):
        """
        list
        以文本形式显示当前编辑的内容。
        """
        if not check_has_load():
            return
        input_history.append('list' + opt)
        list_command = ListCommand()
        list_command.execute()

    @staticmethod
    def do_list_tree(opt):
        """
        list_tree
        以树形结构显示当前编辑的内容。
        """
        if not check_has_load():
            return
        input_history.append('list-tree' + opt)
        list_command = ListTreeCommand()
        list_command.execute()

    @staticmethod
    def do_dir_tree(opt):
        """
        dir_tree [目录名]
        以树形结构显示指定目录（标题）下的内容。
        """
        if not check_has_load():
            return
        input_history.append('dir-tree' + opt)
        list_command = DirTreeCommand(opt)
        list_command.execute()

    def do_insert(self, opt):
        """
        insert [行号] 标题/文本

        行号可以省略，若省略则默认在文件末尾插入内容
        """
        input_history.append('insert' + ' ' + opt)
        # print(input_history)
        if not check_has_load():
            return
        if not check_opt_num(opt, 1):  # 至少一个参数
            return
        insert_command = InsertCommand(opt)
        command_stack.append(insert_command)
        # print(command_stack)
        insert_command.execute()
        self.redo_command = None

    def do_append_head(self, opt):
        """
        append_head 标题/文本

        在文件起始位置插入标题或文本。
        """

        opt = '1' + ' ' + opt
        self.do_insert(opt)

    def do_append_tail(self, opt):
        """
        append-tail 标题/文本

        在文件末尾位置插入标题或文本。
        """
        self.do_insert(opt)

    def do_delete(self, opt):
        """
        delete 标题/文本 或 delete 行号

        如果指定行号，则删除指定行。
        当删除的是标题时，其子标题和内容不会被删除。
        对多个一样的行，只会删除第一个
        """
        input_history.append('delete' + opt)
        if not check_has_load():
            return
        if not check_opt_num(opt, 1):  # 至少一个参数
            return
        delete_command = DeleteCommand(opt)
        command_stack.append(delete_command)
        delete_command.execute()
        self.redo_command = None

    def do_undo(self, opt):
        """
        undo
        撤销上一次执行的编辑命令，返回到执行该命令前的状态。不适用于非编辑命令。
        """
        input_history.append('undo' + opt)
        if len(command_stack) == 0:
            return
        c = command_stack.pop()  # pop()删除并返回末尾元素。
        c.undo()

        undo_tag = UndoCommand()
        command_stack.append(undo_tag)
        # 定义全局变量，用于保存undo之前的一个命令
        self.redo_command = c

    def do_redo(self, opt):
        """
        redo
        只有上一个编辑命令是 undo 时，才允许执行 redo。
        """
        input_history.append('redo' + opt)
        if self.redo_command is None or len(command_stack) == 0:
            print("prompt: no command to redo")
            return
        else:
            # redo就是对undo的命令重新执行一遍，执行完后清空redo_command中的内容
            self.redo_command.execute()
            self.redo_command = None

    argparse_stats = aps.ArgumentParser()
    argparse_stats.add_argument('choose', nargs='?', default='current', type=str, help='path of file')

    def do_stats(self, line):
        """
        stats [all | current]
        all 或 current 参数可选。
        显示当前回话中指定文件或所有文件的工作时长统计。默认为 `current`，显示当前文件的统计信息
        """
        f = open(constant.LOG_DIR, 'a', encoding='utf-8')
        now_time = int(time.time())
        try:
            args = self.argparse_stats.parse_args(line.split())

            if args.choose == 'all':
                # 遍历所有文件计算工作时长并显示
                for start_time in start_times:
                    seconds = now_time - start_times[start_time]
                    s = start_time + cal_time(seconds)
                    f.write(s + '\n')
                    print(s)
            else:
                # 确保当前文件存在
                assert current_load_file != '', 'No current file.'
                # 显示当前文件的工作时长
                seconds = now_time - start_times[current_load_file]
                s = current_load_file + cal_time(seconds)
                f.write(s + '\n')
                print(s)

        except Exception as e:
            print(f'Error: {e}')

        f.close()

    def set_prompt(self, line):
        self.prompt = line
        return self


def main():
    welcome = "\n\
    ***********************************************************************************\n\
       __  __            _       _                       ______    _ _ _               \n\
      |  \/  |          | |     | |                     |  ____|  | (_) |              \n\
      | \  / | __ _ _ __| | ____| | _____      ___ __   | |__   __| |_| |_ ___  _ __   \n\
      | |\/| |/ _` | '__| |/ / _` |/ _ \ \ /\ / / '_ \  |  __| / _` | | __/ _ \| '__|  \n\
      | |  | | (_| | |  |   < (_| | (_) \ V  V /| | | | | |___| (_| | | || (_) | |     \n\
      |_|  |_|\__,_|_|  |_|\_\__,_|\___/ \_/\_/ |_| |_| |______\__,_|_|\__\___/|_|     \n\
                                                                                       \n\
    ***********************************************************************************\n\
    "
    print(welcome)
    session_time = time.strftime('%Y%m%d %H%M%S', time.localtime())

    if not os.path.exists(constant.LOG_DIR):
        print("prompt: file not exist, create file: " + constant.LOG_DIR)
        f = open(constant.LOG_DIR, 'a', encoding='utf-8')
        f.write('session start ' + session_time)
        f.close()
    else:
        f = open(constant.LOG_DIR, 'a', encoding='utf-8')
        f.write('session start ' + session_time + '\n')
        f.close()
    NewInput().set_prompt("<Editor> ").cmdloop()


if __name__ == '__main__':
    main()
