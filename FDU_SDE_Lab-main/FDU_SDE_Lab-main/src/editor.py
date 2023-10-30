import os
import shutil

import constant

__all__ = [constant]

# 注意路径，有可能需要修改为"../data"
constant.WORKPATH = "./data"
constant.TEMP_FILE = "temp_file.md"


# load 文件路径
# 从指定路径加载文件到工作区
# 如果指定的文件不存在，则新建一个文件
def ed_load(file_path):
    # 检查目标文件，不存在则创建，
    if not os.path.exists(file_path):
        print("prompt: file not exist, create file: " + file_path)
        f = open(file_path, 'w', encoding='utf-8')
        f.close()
    # 将目标文件复制到工作区
    try:
        if os.path.exists(os.path.join(constant.WORKPATH, constant.TEMP_FILE)):
            os.remove(os.path.join(constant.WORKPATH, constant.TEMP_FILE))
        shutil.copyfile(file_path, os.path.join(constant.WORKPATH, constant.TEMP_FILE))
        return True
    except IOError as e:
        print("error: unable to create temp_file when loading file. %s" % e)
        return False


# save
# 将工作区文件保存到之前加载的或新创建的文件中
def ed_save(file_path):
    # 确保有一个文件已经被加载或创建
    if not os.path.exists(file_path):
        print("error: file not exist.")
        return
    # 将工作区临时文件写回到源文件
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        shutil.copyfile(os.path.join(constant.WORKPATH, constant.TEMP_FILE), file_path)
    except IOError:
        print("error: unable to save file: " + file_path)


# read
# 简单地读取当前文件
def ed_read():
    f = open(os.path.join(constant.WORKPATH, constant.TEMP_FILE), 'r+', encoding='utf-8')
    print(f.read())
    f.close()


# insert [行号] 标题/文本
# 在指定行插入标题或文本。如果不指定行号，则默认在文件的最后一行插入内容。
# 行号参数可选, 若 insert 后面可以用空格分为head + tail，并且head是数字，那head就当行号来处理
# 如果行号大于当前总行数，转换为文件末尾插入的命令。
# 返回实际插入的行号，失败则返回-1
def ed_insert(opt):
    f = open(os.path.join(constant.WORKPATH, constant.TEMP_FILE), 'a+', encoding='utf-8')
    # 获取文件f的总行数
    f.seek(0, 0)
    line_count = len(f.readlines())

    opt1 = opt.split(' ')[0]
    if opt1.isdigit():
        # 判定第一个参数为数字（指定行号）
        if len(opt.split(' ', 1)) < 2:
            print("prompt: lack insert content")
            return -1
        content = opt.split(' ', 1)[1]  # content为插入的内容
        # 判定行号大于当前总行数, 则直接写入末尾
        if int(opt1) > line_count:
            if not line_count == 0:
                f.write('\n')
            f.write(content)
            f.close()
            return line_count + 1
        else:
            insert_location = int(opt1)
    else:
        # 不指定行号，则直接插入到文件末尾
        content = opt
        if not line_count == 0:
            f.write('\n')
        f.write(content)
        f.close()
        return line_count + 1

    lines = []
    f.seek(0, 0)
    for s in f:
        lines.append(s)  # 将每一行的数据添加到列表
    lines.insert(insert_location - 1, content + '\n')  # 插入数据
    f = open(os.path.join(constant.WORKPATH, constant.TEMP_FILE), 'w', encoding='utf-8')  # 清空文件
    f.writelines(lines)  # 将修改后的数据写回原文件
    f.close()
    return insert_location


# delete 标题/文本 或 delete 行号
# 如果指定行号，则删除指定行。
# 当删除的是标题时，其子标题和内容不会被删除。
# 返回删除位置和删除内容
def ed_delete(opt):
    f = open(os.path.join(constant.WORKPATH, constant.TEMP_FILE), 'a+', encoding='utf-8')
    lines = []
    f.seek(0, 0)
    for s in f:
        lines.append(s)  # 将每一行的数据添加到列表

    delete_location = -1
    if opt.isdigit():  # 判断opt是否为数字
        delete_location = int(opt)
        delete_content = lines[delete_location - 1].strip('\n')
    else:  # 找第一个匹配的位置
        delete_content = opt
        if opt + '\n' in lines:
            delete_location = lines.index(opt + '\n') + 1
        elif opt in lines:
            delete_location = lines.index(opt) + 1
        else:
            print("prompt: can not find delete content: " + opt)
    if delete_location == -1:
        return delete_location, delete_content

    del lines[delete_location - 1]
    # 如果要删除的标题是最后一行，则删除后不需要再添加换行符
    if delete_location == len(lines) + 1 and len(lines) > 0:
        lines[len(lines) - 1] = lines[len(lines) - 1].strip('\n')
    f = open(os.path.join(constant.WORKPATH, constant.TEMP_FILE), 'w', encoding='utf-8')
    f.writelines(lines)
    return delete_location, delete_content
