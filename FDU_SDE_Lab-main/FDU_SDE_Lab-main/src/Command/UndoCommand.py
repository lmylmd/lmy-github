# 定义具体实现类
from Command.CommandAbs import CommandAbs


class UndoCommand(CommandAbs):
    # 仅仅用作记号
    def execute(self):
        pass

    def undo(self):
        pass
