import subprocess
import sys
import oss2
import os

#登录信息
endpoint = ''
accesskey_id = ""
accesskey_secret = ""
bucket_name = ""

# 本地文件保存路径前缀
download_local_save_prefix = ""
root_dir_list = []
'''
列举prefix全部文件
'''


def prefix_all_list(bucket, prefix):
    # print("开始列举" + prefix + "全部文件")
    oss_file_size = 0
    for obj in oss2.ObjectIterator(bucket):


        # print(' key : ' + obj.key)
        if str(obj.key).endswith('/'):
            # print("D " +obj.key)
            try:
                str1 =str(f"{download_local_save_prefix}\\"+obj.key)
                dir = str1.replace("\\","/")
                # print(dir)
                os.mkdir(dir)
            except FileExistsError:
                pass

        else:
            # print("F: "+obj.key)
            download_to_local(bucket, obj.key)

def prefix_all_list_md5(bucket, prefix):
    # print("开始列举" + prefix + "全部文件")
    oss_file_size = 0
    for obj in oss2.ObjectIterator(bucket):

        # print(' key : ' + obj.key)
        if str(obj.key).endswith('/'):
            # print("D " +obj.key)
            try:
                str1 = str(f"{download_local_save_prefix}\\" + obj.key)
                dir = str1.replace("\\", "/")
                # print(dir)
                os.mkdir(dir)
            except FileExistsError:
                pass

        elif str(obj.key).endswith("MD5.txt" ) :
            # print("F: "+obj.key)
            download_to_local(bucket, obj.key)




    # print(prefix + " file size " + str(oss_file_size))


'''
列举全部的根目录文件夹、文件
'''


def root_directory_list(bucket):
    # 设置Delimiter参数为正斜线（/）。
    num = 0
    for obj in oss2.ObjectIterator(bucket, delimiter='/'):
        # 通过is_prefix方法判断obj是否为文件夹。
        if obj.is_prefix():  # 文件夹
            global root_dir
            root_dir= f"{download_local_save_prefix}/{obj.key}"
            # print(root_dir)
            # print(root_dir)
            # print('directory: ' + obj.key)
            # print(str(obj.key).strip("/"))
            prefix_all_list(bucket, str(obj.key).strip("/")) # 去除/
        else:  # 文件
            # print('file: ' + obj.key)
            # 下载根目录的单个文件
            download_to_local(bucket, str(obj.key))
            num += 1
            print(num)
def root_directory_list_md5(bucket):
    # 设置Delimiter参数为正斜线（/）。
    num = 0
    for obj in oss2.ObjectIterator(bucket, delimiter='/'):
        # 通过is_prefix方法判断obj是否为文件夹。
        if obj.is_prefix():  # 文件夹
            global root_dir
            root_dir = f"{download_local_save_prefix}/{obj.key}"
            prefix_all_list_md5(bucket, str(obj.key).strip("/"))
        else:  # 文件
            # print('file: ' + obj.key)
            # 下载根目录的单个文件
            download_to_local(bucket, str(obj.key))
            num += 1
            # print(num)


'''
下载文件到本地
'''



def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        # rate表示下载进度。
        print('\r{0}% '.format(rate), end='')

        sys.stdout.flush()
def download_to_local(bucket, object_name):
    url = download_local_save_prefix
    # print(object_name)
    # 文件名称
    # file_name = url[url.rindex("/") + 1:]

    # file_path_prefix = url.replace(file_name, "")
    # if False == os.path.exists(object_name):
    #     os.makedirs(file_path_prefix)
    #     print("directory don't not makedirs " + file_path_prefix)

    # 下载OSS文件到本地文件。如果指定的本地文件存在会覆盖，不存在则新建。
    list = [download_local_save_prefix,object_name]
    down_dir ="/".join(list)
    dir = down_dir.replace("\\","/")
    print(object_name)
    bucket.get_object_to_file(object_name, dir, progress_callback=percentage)
    print("")


if __name__ == '__main__':
    command_list = ["-d", "-ak", "-as", "-ep", "-b"]



    # 本地文件保存路径前缀
    # download_local_save_prefix = "D:/EXAMPLEEEEEEE"
    if "-d" in sys.argv:
        try:
            j = sys.argv.index("-d")
            download_local_save_prefix = sys.argv[j + 1]
        except IndexError:
            pass
    else:
        pass

    if "-b" in sys.argv:
        try:
            j = sys.argv.index("-b")
            bucket_name = sys.argv[j + 1]
        except IndexError:
            pass
    else:
        pass

    if "-ak" in sys.argv:
        try:
            j = sys.argv.index("-ak")
            accesskey_id = sys.argv[j + 1]
        except IndexError:
            pass
    else:
        pass

    if "-as" in sys.argv:
        try:
            j = sys.argv.index("-as")
            accesskey_secret = sys.argv[j + 1]
        except IndexError:
            pass
    else:
        pass

    if "-ep" in sys.argv:
        try:
            j = sys.argv.index("-ep")
            endpoint = sys.argv[j + 1]
        except IndexError:
            pass
    else:
        pass







    print("start \n")
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth(accesskey_id, accesskey_secret)
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    # 单个文件夹下载
    #prefix_all_list(bucket, "20201223")
    try:
        os.mkdir(download_local_save_prefix)
    except FileExistsError:
        pass
    root_directory_list_md5(bucket)
    data_dir_list = os.listdir(root_dir)
    # print(data_dir_list)
    for dir in data_dir_list:
        print(f"python file_check.py -d {root_dir}{dir}")
        subprocess.Popen(["D:\\Git\\git-bash.exe", "-c", f"python file_check.py -d {root_dir}{dir}"])
    root_directory_list(bucket)

    # print(root_dir)


    print("end \n")