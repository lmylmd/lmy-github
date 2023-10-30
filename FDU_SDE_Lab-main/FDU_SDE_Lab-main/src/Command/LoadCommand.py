# 定义具体实现类
import editor
# import CommandAbs
from Command.CommandAbs import CommandAbs


class LoadCommand(CommandAbs):
    def __init__(self, opt):
        # 接收者为 editor (import editor)
        self.opt = opt

    def execute(self):
        return editor.ed_load(self.opt)  # load success or fail

    def undo(self):
        print("prompt: load command can not undo ")
