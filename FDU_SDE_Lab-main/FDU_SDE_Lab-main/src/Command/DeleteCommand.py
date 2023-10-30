# 定义具体实现类
import editor
# import CommandAbs
from Command.CommandAbs import CommandAbs


class DeleteCommand(CommandAbs):
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
