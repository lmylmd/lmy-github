from abc import ABC, abstractmethod


# import editor

# 定义抽象类
class CommandAbs(ABC):
    @abstractmethod
    def execute(self):  # 实现执行命令逻辑
        pass

    @abstractmethod
    def undo(self):  # 实现命令撤销
        pass
