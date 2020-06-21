import pandas as pd
import numpy as np

import jieba as jb

base_path = "C:/Users/matt/PycharmProjects/JustTest/resource/"
out_path = "C:/Users/matt/Documents/数据导入与预处理/实验/第一节课"
data = pd.read_csv(f"{base_path}/数据导入与预处理_18级_20200621152835.csv")

all_column_names = [
    "data_id",  # 0
    "班级",  # 1
    "性别",  # 2
    "出生日期",  # 3
    "年龄",  # 4
    "年级",  # 5
    "是否喜欢编程？",  # 6
    "是否写过程序？",  # 7
    "熟悉下面哪些编程语言？",  # 8
    "熟悉下面哪些数据源？",  # 9
    "如果有竞赛实践的项目，是否愿意参加",  # 10
    "学过的课程中，感觉哪些比较实用，可以列举一下",  # 11
    "关于数据导入与预处理，谈谈你的理解",  # 12
    "谈一下对就业市场的了解，和自己的职业规划",  # 13
    "提交时间",  # 14
]
if True:
    use_column_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 10, 14]
    all_values = data.values
    use_values = all_values[:, use_column_indexes]

    new_rows = []
    birthday_index = 3
    age_index = 4
    for row in use_values:
        birthday = row[birthday_index]
        new_row = np.copy(row)
        if birthday is None or "" == birthday:
            new_row[birthday_index] = "2000-01-01"
        age = row[age_index]
        if age is None or "" == age:
            new_row[age_index] = 20
        new_rows.append(new_row)

    save = pd.DataFrame(data=np.array(new_rows), columns=[all_column_names[i] for i in use_column_indexes])
    save.to_csv(f"{out_path}/基础信息表.csv", encoding="UTF-8-sig", index=False, sep=",")
if True:
    # 扩展熟悉的编程语言
    use_column_indexes = [0, 8]
    use_column_names = np.array([all_column_names[i] for i in use_column_indexes])
    use_values = all_values[:, use_column_indexes]

    expand_column_name = all_column_names[8]
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
    # 扩展熟悉的数据源
    use_column_indexes = [0, 9]
    use_column_names = np.array([all_column_names[i] for i in use_column_indexes])
    use_values = all_values[:, use_column_indexes]

    expand_column_name = all_column_names[9]
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
    save.to_csv(f"{out_path}/熟悉的数据源.csv", encoding="UTF-8-sig", index=False, sep=",")

if True:
    # 扩展学过的课程
    use_column_indexes = [0, 11]
    use_column_names = np.array([all_column_names[i] for i in use_column_indexes])
    use_values = all_values[:, use_column_indexes]
    expand_column_name = all_column_names[11]
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
            new_row[expand_column] = l_l.upper()
            new_rows.append(new_row)
    print(len(new_rows))

    save = pd.DataFrame(data=np.array(new_rows), columns=[all_column_names[i] for i in use_column_indexes])
    save.to_csv(f"{out_path}/学过的课程.csv", encoding="UTF-8-sig", index=False, sep=",")

if True:
    # 扩展数据预处理的理解
    use_column_indexes = [0, 12]
    use_column_names = np.array([all_column_names[i] for i in use_column_indexes])
    expand_column_name = all_column_names[12]
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
    save.to_csv(f"{out_path}/数据导入与预处理的理解.csv", encoding="UTF-8-sig", index=False, sep=",")

if True:
    # 扩展职业规划
    use_column_indexes = [0, 13]
    use_column_names = np.array([all_column_names[i] for i in use_column_indexes])
    expand_column_name = all_column_names[13]
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
