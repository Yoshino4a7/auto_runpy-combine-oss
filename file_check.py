import os
import subprocess
import sys
import hashlib
import time
from timeloop import Timeloop
from datetime import timedelta
# import watchdog
# file_execute = {}
#
#
# old_file_list.sort(key=lambda file:os.path.getmtime(os.path.join(dir_name,file)))
# for name in old_file_list:
#     file_execute[name] = False
# print(file_execute)
#
# while True:
#     list = os.listdir(dir_name)
#     new_file_list = [name for name in list if name.endswith(".mp3") and ]
#     file_list.sort(key=lambda file: os.path.getmtime(os.path.join(dir_name, file)))
file_execute_DNA = {}
file_execute_RNA = {}
DNA_dir_list = []
RNA_dir_list = []
mergeRawFq_file_list_RNA ={}
mergeRawFq_file_list_DNA ={}
ok_filelist_DNA = {}
ok_filelist_RNA = {}
def init(old_file_list,option):
    for name in old_file_list.keys():
        if option == 0:
            if (name in file_execute_DNA.keys()) is False:
                file_execute_DNA[name] = False
        if option == 1:
            if (name in file_execute_RNA.keys()) is False:
                file_execute_RNA[name]= False


    # print(file_execute)




# for file_name in old_file_list:
#     os.system(f'md5sum  {file_name}  >> md5sum.txt')
# while True:

def check_file_list():
    # print(mergeRawFq_dir_list)

    if len(mergeRawFq_dir_list) > 0:
        DNA_dir_list = [dir for dir in mergeRawFq_dir_list if dir.startswith("D")]
        RNA_dir_list = [dir for dir in mergeRawFq_dir_list if dir.startswith("R")]

        try:
            for dir in RNA_dir_list:
                file_list = os.listdir(os.path.join(mergeRawFq_dir, dir))

                for name in file_list:
                    # print(mergeRawFq_file_list_RNA.keys())

                    if (name in mergeRawFq_file_list_RNA.keys()) is False:
                        mergeRawFq_file_list_RNA[name] = dir
            init(mergeRawFq_file_list_RNA, 1)
        except:
            pass
        try:
            for dir in DNA_dir_list:
                file_list = os.listdir(os.path.join(mergeRawFq_dir, dir))
                for name in file_list:
                    if (name in mergeRawFq_file_list_DNA) is False :
                        mergeRawFq_file_list_DNA[name] = dir
            init(mergeRawFq_file_list_DNA, 0)
        except:
            pass
    else:
        pass






def md5_check():
    # print(mergeRawFq_file_list_RNA)
    try:
        for name,dir in mergeRawFq_file_list_RNA.items():
            file_dir = os.path.join(os.path.join(mergeRawFq_dir,dir),name)
            with open(f"{file_dir}", "rb") as f:
                content = f.read()
                md5hash = hashlib.md5(content)
                md5 = md5hash.hexdigest()
                # print(md5)

            if (md5 in md5_list) is True:
                if dir[0] == "R":
                    ok_filelist_RNA[name] = dir
                if dir[0] == "D":
                    ok_filelist_DNA[name] = dir
    except:
        pass
    try:
        for name,dir in mergeRawFq_file_list_DNA.items():
            file_dir = os.path.join(os.path.join(mergeRawFq_dir,dir),name)
            with open(f"{file_dir}", "rb") as f:
                content = f.read()
                md5hash = hashlib.md5(content)
                md5 = md5hash.hexdigest()
                # print(md5)
            if (md5 in md5_list) is True:
                if dir[0] == "R":
                    ok_filelist_RNA[name] = dir
                if dir[0] == "D":
                    ok_filelist_DNA[name] = dir
    except:
        pass

def ok_file_run_DNA():
    try:
        # 获得已通过校验的文件序列
        # print(ok_filelist_DNA)
        for name in ok_filelist_DNA.keys():
            if name in file_execute_DNA.keys():
                if file_execute_DNA[name] is True:
                    # 该文件已执行过脚本 略过
                    print(f"The file {name} has ran the DNA.py")

                else:
                    # 该文件执行脚本
                    run_dir = os.path.join(mergeRawFq_dir, ok_filelist_DNA[name])
                    # print(os.path.join(mergeRawFq_dir, ok_filelist_RNA[name]))

                    subprocess.run(f'python {dna_name} {os.path.join(run_dir, name)}')
                    file_execute_DNA[name] = True

            else:
                # 该文件执行脚本
                run_dir = os.path.join(mergeRawFq_dir, ok_filelist_DNA[name])
                # print(os.path.join(mergeRawFq_dir, ok_filelist_RNA[name]))

                subprocess.run(f'python {dna_name} {os.path.join(run_dir, name)}')
                file_execute_DNA[name] = True

    except:
        pass

def ok_file_run_RNA():
    for name in ok_filelist_RNA.keys():
        if name in file_execute_RNA.keys():
            if file_execute_RNA[name] is True:
                # 该文件已执行过脚本 略过
                print(f"The file {name} has ran the RNA.py")

            else:
                # 该文件执行脚本
                run_dir = os.path.join(mergeRawFq_dir, ok_filelist_RNA[name])
                # print(run_dir)
                # print(os.path.join(mergeRawFq_dir, ok_filelist_RNA[name]))
                file_execute_RNA[name] = True
                subprocess.run(f'python {rna_name} {os.path.join(run_dir, name)}')

        else:
            # 该文件执行脚本
            run_dir = os.path.join(mergeRawFq_dir, ok_filelist_RNA[name])
            # print(run_dir)
            # print(os.path.join(mergeRawFq_dir, ok_filelist_RNA[name]))
            file_execute_RNA[name] = True
            subprocess.run(f'python {rna_name} {os.path.join(run_dir, name)}')

def transform_path(path):
    return 1

def loop_task():
    mergeRawFq_dir_list = os.listdir(mergeRawFq_dir)

    check_file_list()
    try:
        md5_check()
    except:
        print("MD5")

    ok_file_run_RNA()
    ok_file_run_DNA()


if __name__== "__main__":
    command_list = ["-d", "--dicrectory","-e","--end","-dna","-rna"]
    dir_name = "."
    dna_name = os.path.abspath("./DNA.py")
    rna_name = os.path.abspath("./RNA.py")
    end_name = ".txt"
    if "-d" in sys.argv:
        try:
            j = sys.argv.index("-d")
            dir_name = sys.argv[j + 1]
        except IndexError:
            pass
    else:
        pass
    if "--dicrectory" in sys.argv:
        try:
            j = sys.argv.index("-d")

            dir_name = sys.argv[j + 1]
        except IndexError:
            pass
    else:
        pass
    if "-e" in sys.argv:
        try:
            j = sys.argv.index("-e")
            end_name = sys.argv[j + 1]
        except IndexError:
            pass
    else:
        pass
    if "--end" in sys.argv:
        try:
            j = sys.argv.index("--end")
            end_name = sys.argv[j + 1]
        except IndexError:
            pass
    else:
        pass
    if "-dna" in sys.argv:
        try:
            j = sys.argv.index("-dna")
            list_dir = "/".join(sys.argv[j + 1].split("\\"))
            # list_dir.insert(2, "\\")
            dna_name = sys.argv[j + 1]
        except IndexError:
            pass
    else:
        pass
    if "-rna" in sys.argv:
        try:
            j = sys.argv.index("-rna")
            # list_dir = list("\\".join(sys.argv[j + 1].split("\\")))
            # list_dir.insert(2, "\\")
            # print(list_dir)
            rna_name = sys.argv[j + 1]

        except IndexError:
            pass
    else:
        pass

    dir_name = os.path.abspath(dir_name).replace("\\","/")
    # print(dir_name)
    flag_dir = dir_nagitgime
    MD5_dir = os.path.join(dir_name, "MD5.txt").replace("\\\\","/")
    mergeRawFq_dir = os.path.join(dir_name, "00.mergeRawFq").replace("\\","/")
    # print(mergeRawFq_dir)
    # mergeRawFq_dir[]="\\"
    global mergeRawFq_dir_list
    mergeRawFq_dir_list = os.listdir(mergeRawFq_dir)
    md5_list = []

    with open(MD5_dir,"r") as md5_file:
        list = md5_file.readlines()
        md5_list = [line[:32] for line in list]
    # print(md5_list)
    #     tl = Timeloop()


        # while 1 == 1:
        #     loop_task()
        #     sys.stdout.flush()
        #     time.sleep(5)
            # print(mergeRawFq_file_list_RNA)
            # try:
            #     if "flag.txt" in os.listdir(flag_dir):
            #
            #     else:
            #         print("The file has not finished")
            # except:
            #     print("The file has not finished")




