import pandas as pd
import numpy as np

import jieba as jb

base_path = "C:/Users/matt/PycharmProjects/JustTest/resource/"
out_path = "C:/Users/matt/Documents/问卷数据"
data = pd.read_csv(f"{base_path}/问卷调查_20200604190856.csv")

all_column_names = [
    "data_id",  # 0
    "班级",  # 1
    "性别",  # 2
    "年级",  # 3
    "是否写过程序？",  # 4
    "是否喜欢编程？",  # 5
    "熟悉下面哪些编程语言？",  # 6
    "如果有竞赛实践的项目，是否愿意参加",  # 7
    "学过的课程中，感觉哪些比较实用，可以列举一下",  # 8
    "谈一下对就业市场的了解，和自己的职业规划",  # 9
    "提交人",  # 10
    "提交时间",  # 11
    "更新时间"  # 12
]
if True:
    use_column_indexes = [0, 1, 2, 3, 4, 5, 6, 7]
    all_values = data.values
    use_values = all_values[:, use_column_indexes]
    class1 = "0864191"
    class2 = "0864192"
    new_rows = []
    class_index = 1
    for row in use_values:
        class_num = row[class_index]
        new_row = np.copy(row)
        if "二班" in class_num or class2 in class_num:
            new_row[class_index] = class2
        else:
            new_row[class_index] = class1
        new_rows.append(new_row)

    save = pd.DataFrame(data=np.array(new_rows), columns=[all_column_names[i] for i in use_column_indexes])
    save.to_csv(f"{out_path}/基础信息表.csv", encoding="UTF-8-sig", index=False, sep=",")
if True:
    # 扩展熟悉的编程语言
    use_column_indexes = [0, 6]
    use_column_names = np.array([all_column_names[i] for i in use_column_indexes])
    use_values = all_values[:, use_column_indexes]

    expand_column_name = all_column_names[6]
    expand_column = np.where(use_column_names == expand_column_name)
    new_rows = []
    for row in use_values:
        programing_languages = row[expand_column][0]
        programing_languages = programing_languages.replace("，", ",")
        p_ls = programing_languages.split(",")
        print(programing_languages)
        for p_l in p_ls:
            new_row = np.copy(row)
            new_row[expand_column] = p_l
            new_rows.append(new_row)
    print(len(new_rows))

    save = pd.DataFrame(data=np.array(new_rows), columns=[all_column_names[i] for i in use_column_indexes])
    save.to_csv(f"{out_path}/熟悉的编程语言.csv", encoding="UTF-8-sig", index=False, sep=",")
if True:
    # 扩展学过的课程
    use_column_indexes = [0, 8]
    use_column_names = np.array([all_column_names[i] for i in use_column_indexes])
    use_values = all_values[:, use_column_indexes]
    expand_column_name = all_column_names[8]
    expand_column = np.where(use_column_names == expand_column_name)
    # use_values = new_rows
    new_rows = []
    for row in use_values:
        lesson_learned = row[expand_column][0]
        lesson_learned = lesson_learned.replace("，", ",")
        lesson_learned = lesson_learned.replace(" ", ",")
        lesson_learned = lesson_learned.replace("、", ",")
        l_ls = lesson_learned.split(",")
        for l_l in l_ls:
            if l_l == "":
                continue
            new_row = np.copy(row)
            new_row[expand_column] = l_l
            new_rows.append(new_row)
    print(len(new_rows))

    save = pd.DataFrame(data=np.array(new_rows), columns=[all_column_names[i] for i in use_column_indexes])
    save.to_csv(f"{out_path}/学过的课程.csv", encoding="UTF-8-sig", index=False, sep=",")

if True:
    # 扩展职业规划
    use_column_indexes = [0, 9]
    use_column_names = np.array([all_column_names[i] for i in use_column_indexes])
    expand_column_name = all_column_names[9]
    expand_column = np.where(use_column_names == expand_column_name)
    use_values = all_values[:, use_column_indexes]
    stopwords_dict = {}.fromkeys(
        [word.strip() for word in
         open(f"{base_path}/stopwords.txt", encoding="utf-8").readlines()])
    # use_values = new_rows
    new_rows = []

    jb.add_word("大数据")
    jb.add_word("算法工程师")
    jb.add_word("数据分析师")
    jb.add_word("开发能力")
    jb.add_word("薪资待遇")

    for row in use_values:
        career_planing = row[expand_column][0]
        key_words = jb.cut(career_planing, HMM=False)
        use_flag = False
        for k_w in key_words:
            if k_w in stopwords_dict or k_w == " " or k_w == "/n":
                continue
            use_flag = True
            new_row = np.copy(row)
            new_row[expand_column] = k_w
            new_rows.append(new_row)
        if not use_flag:
            new_rows.append(row)
    print(len(new_rows))

    save = pd.DataFrame(data=np.array(new_rows), columns=[all_column_names[i] for i in use_column_indexes])
    save.to_csv(f"{out_path}/职业规划表.csv", encoding="UTF-8-sig", index=False, sep=",")
    # todo 拆分成维度表和事实表
