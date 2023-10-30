# 定义具体实现类
import editor
# import CommandAbs
from Command.CommandAbs import CommandAbs


class SaveCommand(CommandAbs):
    def __init__(self, opt):
        self.opt = opt

    def execute(self):
        editor.ed_save(self.opt)

    def undo(self):
        pass
