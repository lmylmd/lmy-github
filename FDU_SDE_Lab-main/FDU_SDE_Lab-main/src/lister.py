import os
import string

import constant


def get_level(line):
    for i in range(1, 7):
        if line.startswith("#" * i + " "):
            return i
    return 7


def set_line(line):
    level = get_level(line)
    if level < 7:
        line = line[1 + level:]
    if line.startswith("* ") or line.startswith("- ") or line.startswith("+ "):
        line = "·" + line[1:]
    return line


def gen_text(line, pre):
    line = set_line(line)
    line = "   " * (pre + 1) + line
    return line


class Lister:
    flags = set()

    def gen_line(self, line, pre, cur, prefix):
        line = set_line(line)
        space_length = cur - pre - 1
        for i in self.flags:
            if pre < i < cur:
                space_length = space_length - 1
        if pre < cur:
            return "   " * pre + prefix + "───" * space_length + line
        else:
            return "   " * (cur - 1) + prefix + line

    def list_tree(self, lines):
        if len(lines) == 0:
            print("None")
            return
        top_level = 7
        for line in lines:
            self.flags.add(get_level(line))
            if get_level(line) < top_level:
                top_level = get_level(line)
        if top_level == 7:
            for line in lines:
                print(line)
        pre_level = 0
        for i, cur in enumerate(lines):
            cur_level = get_level(cur)
            if i == len(lines) - 1:
                if cur_level < 7:
                    cur = self.gen_line(cur, pre_level, cur_level, "└──")
                else:
                    cur = gen_text(cur, pre_level)
                print(cur)
                return
            nxt = lines[i + 1]
            nxt_level = get_level(nxt)
            if cur_level == 7:
                cur = gen_text(cur, pre_level)
                print(cur)
                continue
            if nxt_level == cur_level:
                cur = self.gen_line(cur, pre_level, cur_level, "├──")
                print(cur)
            else:
                cur = self.gen_line(cur, pre_level, cur_level, "└──")
                print(cur)
            pre_level = cur_level


def li_list():
    f = open(os.path.join(constant.WORKPATH, constant.TEMP_FILE), 'r+', encoding='utf-8')
    print(f.read())
    f.close()


def li_list_tree():
    f = open(os.path.join(constant.WORKPATH, constant.TEMP_FILE), 'r+', encoding='utf-8')
    text = f.read()
    lines = text.splitlines()
    Lister().list_tree(lines)
    f.close()


def li_dir_tree(opt: string):
    f = open(os.path.join(constant.WORKPATH, constant.TEMP_FILE), 'r+', encoding='utf-8')
    text = f.read()
    lines = text.splitlines()
    lines_subset = []
    head, tail = None, None
    top_level = 0
    for line in lines:
        if set_line(line) == opt:
            head = line
            top_level = get_level(head)
            lines_subset.append(line)
            continue
        if head is None:
            continue
        if get_level(line) <= top_level:
            break
        lines_subset.append(line)
    if opt.replace(" ", "") == "":
        lines_subset = lines
    Lister().list_tree(lines_subset)
    f.close()
