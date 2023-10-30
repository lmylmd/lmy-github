# 定义具体实现类
import editor
# import CommandAbs
from Command.CommandAbs import CommandAbs


class InsertCommand(CommandAbs):
    def __init__(self, opt):
        self.opt = opt
        self.insert_location = -1

    def execute(self):
        self.insert_location = editor.ed_insert(self.opt)

    def undo(self):
        if not self.insert_location == -1:
            editor.ed_delete(str(self.insert_location))
