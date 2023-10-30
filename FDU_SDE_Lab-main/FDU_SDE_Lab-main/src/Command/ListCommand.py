# 定义具体实现类
import editor
from Command.CommandAbs import CommandAbs


class ListCommand(CommandAbs):
    def execute(self):
        editor.ed_read()

    def undo(self):
        pass
