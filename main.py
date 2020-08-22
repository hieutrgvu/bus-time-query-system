# vn_question = "   Xe bus nào đi đến thành phố Huế lúc 20:00HR ?   "
vn_question = "Thời gian nào xe bus B3 đi từ Đà Nẵng đến thành phố Hồ Chí Minh ?"
# vn_question = "Xe bus nào đi đến thành phố Hồ Chí Minh ?"
# vn_question = "Những xe bus nào đi đến Huế ?"
# vn_question = "Những xe nào xuất phát từ thành phố Hồ Chí Minh ?"
# vn_question = "Những xe nào đi từ Đà nẵng đến thành phố Hồ Chí Minh ?"

################### a. Xây dựng quan hệ văn phạm #######################################################################

# all lowercase
vn_token_dict = {
    # add for question: Xe bus nào đi đến thành phố Huế lúc 20:00HR ?
    "xe bus": ("N", "BUS"),
    "nào": ("WH", "NÀO"),
    "đi": ("V", "ĐI"),
    "đến": ("P", "ĐẾN"),
    "thành phố huế": ("CITY", "HUE"),
    "lúc": ("P", "LÚC"),
    "20:00hr": ("TIME", "20:00HR"),

    # add for question: Thời gian nào xe bus B3 đi từ Đà Nẵng đến Huế ?
    "thời gian": ("TIME", "RUN-TIME"),
    "b3": ("N", "B3"),
    "từ": ("P", "TỪ"),
    "đà nẵng": ("CITY", "DANANG"),
    "huế": ("CITY", "HUE"),

    # add for question: Xe bus nào đi đến thành phố Hồ Chí Minh ?
    "thành phố hồ chí minh": ("CITY", "HCMC"),

    # add for question: Những xe bus nào đi đến Huế ?
    "những xe bus": ("N", "BUS"),

    # add for question: Những xe nào xuất phát từ thành phố Hồ Chí Minh ?
    "những xe": ("N", "BUS"),
    "xuất phát": ("V", "XUẤTPHÁT"),

    # add for question: Những xe nào đi từ Đà nẵng đến thành phố Hồ Chí Minh ?
    # Nothing
}

vn_preposition_type = {
    "từ": "SOURCE",
    "đến": "DEST",
    "lúc": "TIME",
}

dependency_dict = {
    "N_WH": ("right_arc", "nmod"),
    "N_V": ("left_arc", "nsubj"),
    "P_CITY": ("left_arc", "case"),
    "V_CITY": ("right_arc", "nmod"),
    "V_TIME": ("right_arc", "tmod"),
    "N_N": ("right_arc", "nmod"),
    "P_TIME": ("left_arc", "case"),
    "TIME_WH": ("right_arc", "nmod"),
    "TIME_V": ("left_arc", "tmod"),
}

database = {
    "BUS": {"B1", "B2", "B3", "B4"},
    "ATIME": {
        "B1 HUE 22:00HR",
        "B2 HUE 22:30HR",
        "B3 HCMC 05:00HR",
        "B4 HCMC 05:30HR",
        "B5 DANANG 13:30HR",
        "B6 DANANG 09:30HR",
        "B7 HCMC 20:30HR",
    },
    "DTIME": {
        "B1 HCMC 10:00HR",
        "B2 HCMC 12:30HR",
        "B3 DANANG 19:00HR",
        "B4 DANANG 17:30HR",
        "B5 HUE 8:30HR",
        "B6 HUE 5:30HR",
        "B7 HUE 8:30HR",
    },
    "RUNTIME": {
        "B1 HCMC HUE 12:00HR",
        "B2 HCMC HUE 10:00HR",
        "B3 DANANG HCMC 14:00HR",
        "B4 HCMC DANANG 12:00HR",
        "B5 DANANG HUE 5:00HR",
        "B6 DANANG HUE 4:00HR",
        "B7 HCMC HUE 12:00HR",
    },
}


# Always choose the largest token in dict. Example:
# question: "xe bus nào"; token_dict: {"xe": "N", "xe bus": "N", "nào": "WH" } --> output: ["xe bus", "nào"]
def get_question_token(question):
    question = question.rstrip().lstrip().lower()  # remove trailing/leading spaces and convert to lowercase
    if question[-1] == "?": question = question[:-1].rstrip()  # remove "?" character
    question_words = question.split(" ")
    question_num_words = len(question_words)

    question_tokens, start_idx = [], 0
    while start_idx < question_num_words:
        for end_idx in range(question_num_words, start_idx, -1):
            token = " ".join(question_words[start_idx:end_idx])
            if token in vn_token_dict:
                start_idx = end_idx
                question_tokens.append(token)
                break
        else:
            exit("Error: Cannot tokenize the question!")

    return question_tokens


def get_dependency(token_lst):
    stack, dependency, idx = [], [], 0
    while idx < len(token_lst):
        if not stack:
            stack.append(token_lst[idx])
            idx += 1
            continue

        relation = vn_token_dict.get(stack[-1])[0] + "_" + vn_token_dict.get(token_lst[idx])[0]
        if relation in dependency_dict:
            if dependency_dict[relation][0] == "left_arc":
                dependency.append("{}({},{})".format(dependency_dict[relation][1], token_lst[idx], stack[-1]))
                stack.pop()
                continue
            else:  # right_arc
                dependency.append("{}({},{})".format(dependency_dict[relation][1], stack[-1], token_lst[idx]))
        else: stack.append(token_lst[idx])
        idx += 1

    return dependency


vn_question_tokens = get_question_token(vn_question)
vn_question_depend = get_dependency(vn_question_tokens)
with open('output_a.txt', 'w') as writer:
    writer.writelines("+ Tokens: {}\n".format(vn_question_tokens))
    writer.writelines("+ Dependency: {}\n".format(vn_question_depend))


################### b. Tạo dạng luận lý ################################################################################

# Logical form for "print all" case:
# WH : restriction-proposition proposition-body (WHx: Rx Px)
class LogicalFormWH:
    def __init__(self, r=[], p=[]):
        self.r, self.p = r, p

    def __str__(self):
        return "WH x: (&{}) {}".format("".join(self.r), "".join(self.p))


def parse_dependency_code(dependency):
    relation = dependency.split("(")
    word_1st = relation[1].split(",")
    word_2nd = word_1st[1].split(")")
    return relation[0], word_1st[0], word_2nd[0]


vn_question_logical_form, idx = LogicalFormWH(), 1

# Check if this is the valid question
relation, word_1st, word_2nd = parse_dependency_code(vn_question_depend[0])
if relation != "nmod" and word_2nd != "nào":
    exit("Invalid question: Câu hỏi phải bắt đầu bằng 'x nào'!")
vn_question_logical_form.r.append("({} x)".format(vn_token_dict[word_1st][1]))

while idx < len(vn_question_depend):
    relation, word_1st, word_2nd = parse_dependency_code(vn_question_depend[idx])
    if relation == "nsubj":
        vn_question_logical_form.p.append("({} x)".format(word_1st.upper().replace(" ","")))
    elif relation == "case":
        if word_2nd not in vn_preposition_type:
            exit("Giới từ phải được định nghĩa kiểu trong vn_preposition_type")
        vn_question_logical_form.r.append("({} x {})".format(vn_preposition_type[word_2nd], vn_token_dict[word_1st][1]))
        idx += 1  # skip the next nmod because already handled by case relation
    elif relation == "nmod":
        vn_question_logical_form.r.append("({} {} x)".format(vn_token_dict[word_1st][1], vn_token_dict[word_2nd][1]))
    idx += 1

with open('output_b.txt', 'w') as writer:
    writer.writelines("+ Logical Form: {}\n".format(vn_question_logical_form.__str__()))



################### c. Tạo dạng ngữ nghĩa thủ tục ######################################################################

# Check the question type
if vn_question_logical_form.r[0].split(" ")[0].replace("(","") == "BUS":
    vn_question_procedural, idx = [vn_question_logical_form.r[0]], 1
    while idx < len(vn_question_logical_form.r):
        role = vn_question_logical_form.r[idx].split(" ")[0].replace("(", "")
        next_role = vn_question_logical_form.r[idx + 1].split(" ")[0].replace("(", "") if idx + 1 < len(
            vn_question_logical_form.r) else ""
        if role == "DEST":
            d = vn_question_logical_form.r[idx].split(" ")[-1][:-1]
            vn_question_procedural.append("(ATIME x {} ?t)".format(d))
        elif role == "SOURCE":
            s = vn_question_logical_form.r[idx].split(" ")[-1][:-1]
            vn_question_procedural.append("(DTIME x {} ?t)".format(s))
        elif role == "TIME":
            t = vn_question_logical_form.r[idx].split(" ")[-1][:-1]
            vn_question_procedural[-1] = vn_question_procedural[-1].replace("?t", t)
        idx += 1
    with open('output_c.txt', 'w') as writer:
        writer.writelines("+ Procedural Form: (PRINT x {})\n".format("".join(vn_question_procedural)))
else:
    vn_question_procedural, idx = "(RUNTIME ?b ?s ?d ?t)", 0
    while idx < len(vn_question_logical_form.r):
        role = vn_question_logical_form.r[idx].split(" ")[0].replace("(", "")
        if role == "DEST":
            d = vn_question_logical_form.r[idx].split(" ")[-1][:-1]
            vn_question_procedural = vn_question_procedural.replace("?d", d)
        elif role == "SOURCE":
            s = vn_question_logical_form.r[idx].split(" ")[-1][:-1]
            vn_question_procedural = vn_question_procedural.replace("?s", s)
        elif role == "BUS":
            b = vn_question_logical_form.r[idx].split(" ")[1]
            vn_question_procedural = vn_question_procedural.replace("?b", b)
        idx += 1
    with open('output_c.txt', 'w') as writer:
        writer.writelines("+ Procedural Form: (PRINT t {})\n".format(vn_question_procedural))


################### d. Trả lời câu truy vấn ############################################################################

# Check the question type
if vn_question_logical_form.r[0].split(" ")[0].replace("(","") == "BUS":
    bus_list = {
        "ATIME": [False, set()],
        "DTIME": [False, set()],
    }
    for idx in range(1, len(vn_question_procedural)):
        parsed_data = vn_question_procedural[idx].split(" ")
        procedure, loc, time = parsed_data[0].replace("(", ""), parsed_data[2], parsed_data[3].replace(")", "")
        bus_list[procedure][0] = True
        for data in database[procedure]:
            data_bus, data_loc, data_time = data.split(" ")
            if (data_loc == loc) and (data_time == time or time == "?t"):
                bus_list[procedure][1].add(data_bus)

    ans = database["BUS"]
    for ans_lst in bus_list.values():
        if ans_lst[0]:
            ans = ans.intersection(ans_lst[1])
    with open('output_d.txt', 'w') as writer:
        writer.writelines("+ Answer: {}\n".format(ans if ans else None))

else:
    procedure, bus, source, dest, time = vn_question_procedural.split(" ")
    procedure, time = procedure.replace("(", ""), time.replace(")", "")
    ans = None
    for data in database[procedure]:
        data_bus, data_source, data_dest, data_time = data.split(" ")
        if bus == data_bus and source == data_source and dest == data_dest:
            ans = data_time

    with open('output_d.txt', 'w') as writer:
        writer.writelines("+ Answer: {}\n".format(ans))