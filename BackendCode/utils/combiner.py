import sys
from pathlib import Path


path=str(Path(__file__).resolve().parent.parent)
sys.path.append(path)
print(path)

from config.settings import Raw_Data_DIR


output_file = Raw_Data_DIR/"merged_output.txt"



def merge_specific_txt_files(input_folder, filenames, output_filename):
    # 确保输入文件夹路径有效
    if not input_folder.exists() or not input_folder.is_dir():
        print(f"指定的文件夹路径不存在: {input_folder}")
        return

    # 打开输出文件
    with open(str(output_filename), 'w', encoding='utf-8') as outfile:
        for filename in filenames:
            file_path = input_folder / filename
            if file_path.exists() and file_path.is_file():
                print(f"正在合并文件: {file_path}")
                # 读取并写入文件内容
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")  # 添加换行符以区分文件
            else:
                print(f"文件未找到: {file_path}")

    print(f"所有指定的 .txt 文件已合并到: {output_filename}")


if __name__=="__main__":
    # 定义需要合并的文件名列表
    file_list = ["a.txt", "b.txt"]
    # 调用函数进行合并
    merge_specific_txt_files(Raw_Data_DIR, file_list, output_file)