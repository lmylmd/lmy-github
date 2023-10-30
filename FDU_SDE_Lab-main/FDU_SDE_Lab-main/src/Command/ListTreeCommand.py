import lister
from Command.CommandAbs import CommandAbs


class ListTreeCommand(CommandAbs):
    def execute(self):
        lister.li_list_tree()

    def undo(self):
        return
