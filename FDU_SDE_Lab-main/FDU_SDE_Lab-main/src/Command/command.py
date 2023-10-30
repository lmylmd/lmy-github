from abc import ABC, abstractmethod

import editor
import lister


# 定义抽象类
class Command(ABC):
    @abstractmethod
    def execute(self):  # 实现执行命令逻辑
        pass

    @abstractmethod
    def undo(self):  # 实现命令撤销
        pass


# 定义具体实现类
class LoadCommand(Command):
    def __init__(self, opt):
        # 接收者为 editor (import editor)
        self.opt = opt

    def execute(self):
        return editor.ed_load(self.opt)  # load success or fail

    def undo(self):
        print("prompt: load command can not undo ")


class SaveCommand(Command):
    def __init__(self, opt):
        self.opt = opt

    def execute(self):
        editor.ed_save(self.opt)

    def undo(self):
        pass


class ListCommand(Command):
    def execute(self):
        lister.li_list()

    def undo(self):
        pass


class ListTreeCommand(Command):
    def execute(self):
        lister.li_list_tree()

    def undo(self):
        pass


class DirTreeCommand(Command):
    def __init__(self, opt):
        self.opt = opt

    def execute(self):
        lister.li_dir_tree(self.opt)

    def undo(self):
        pass


class InsertCommand(Command):
    def __init__(self, opt):
        self.opt = opt
        self.insert_location = -1

    def execute(self):
        self.insert_location = editor.ed_insert(self.opt)

    def undo(self):
        if not self.insert_location == -1:
            editor.ed_delete(str(self.insert_location))


class DeleteCommand(Command):
    def __init__(self, opt):
        self.opt = opt
        self.delete_location = -1
        self.delete_content = -1

    def execute(self):
        (self.delete_location, self.delete_content) = editor.ed_delete(self.opt)

    def undo(self):
        if not self.delete_location == -1:
            # print((str(self.delete_location) + ' ' + str(self.delete_content)))
            editor.ed_insert(str(self.delete_location) + ' ' + str(self.delete_content))


class UndoCommand(Command):
    # 仅仅用作记号
    def execute(self):
        pass

    def undo(self):
        pass
