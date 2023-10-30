import lister
from Command.CommandAbs import CommandAbs


class DirTreeCommand(CommandAbs):
    def __init__(self, opt):
        self.opt = opt

    def execute(self):
        lister.li_dir_tree(self.opt)

    def undo(self):
        return
