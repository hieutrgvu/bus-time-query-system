import os
from Input.question import vn_question
from Input.database import vn_dictionary, vn_preposition_type, dependency_dict, database

################### a. Xây dựng quan hệ văn phạm #######################################################################


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
            if token in vn_dictionary:
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

        relation = vn_dictionary.get(stack[-1])[0] + "_" + vn_dictionary.get(token_lst[idx])[0]
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

if not os.path.exists("Output"):
    os.makedirs("Output")
with open('Output/output_a.txt', 'w') as writer:
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
vn_question_logical_form.r.append("({} x)".format(vn_dictionary[word_1st][1]))

while idx < len(vn_question_depend):
    relation, word_1st, word_2nd = parse_dependency_code(vn_question_depend[idx])
    if relation == "nsubj":
        vn_question_logical_form.p.append("({} x)".format(word_1st.upper().replace(" ","")))
    elif relation == "case":
        if word_2nd not in vn_preposition_type:
            exit("Giới từ phải được định nghĩa kiểu trong vn_preposition_type")
        vn_question_logical_form.r.append("({} x {})".format(vn_preposition_type[word_2nd], vn_dictionary[word_1st][1]))
        idx += 1  # skip the next nmod because already handled by case relation
    elif relation == "nmod":
        vn_question_logical_form.r.append("({} {} x)".format(vn_dictionary[word_1st][1], vn_dictionary[word_2nd][1]))
    idx += 1

with open('Output/output_b.txt', 'w') as writer:
    writer.writelines("+ Logical Form: {}\n".format(vn_question_logical_form.__str__()))


################### c. Tạo dạng ngữ nghĩa thủ tục ######################################################################

# Check the question type
if vn_question_logical_form.r[0].split(" ")[0].replace("(","") == "BUS":
    vn_question_procedural, idx = ["(BUS b)"], 1
    while idx < len(vn_question_logical_form.r):
        role = vn_question_logical_form.r[idx].split(" ")[0].replace("(", "")
        next_role = vn_question_logical_form.r[idx + 1].split(" ")[0].replace("(", "") if idx + 1 < len(
            vn_question_logical_form.r) else ""
        if role == "DEST":
            d = vn_question_logical_form.r[idx].split(" ")[-1][:-1]
            vn_question_procedural.append("(ATIME b {} ?t)".format(d))
        elif role == "SOURCE":
            s = vn_question_logical_form.r[idx].split(" ")[-1][:-1]
            vn_question_procedural.append("(DTIME b {} ?t)".format(s))
        elif role == "TIME":
            t = vn_question_logical_form.r[idx].split(" ")[-1][:-1]
            vn_question_procedural[-1] = vn_question_procedural[-1].replace("?t", t)
        idx += 1

    vn_question_procedural_txt = "(PRINT b {})".format("".join(vn_question_procedural))
    with open('Output/output_c.txt', 'w') as writer:
        writer.writelines("+ Procedural Form: {}\n".format(vn_question_procedural_txt))
else:
    # Assume it is run-time query, but if ?s and ?d is not filled, it will be converted to time query later
    vn_question_procedural, idx = "(RUN-TIME ?b ?s ?d ?t)", 0
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
    vn_question_procedural_txt = "(PRINT t {})".format(vn_question_procedural)

    # Converted to time query if ?s and ?d is not filled
    if "?s" in vn_question_procedural and "?d" in vn_question_procedural:
        exit("Invalid question!")
    elif "?s" in vn_question_procedural:
        procedure, bus, source, dest, time = vn_question_procedural.split(" ")
        vn_question_procedural = ["(BUS {})".format(bus), "(ATIME {} {} t)".format(bus, dest)]
        vn_question_procedural_txt = "(PRINT t {})".format("".join(vn_question_procedural))
    elif "?d" in vn_question_procedural:
        procedure, bus, source, dest, time = vn_question_procedural.split(" ")
        vn_question_procedural = ["(BUS {})".format(bus), "(DTIME {} {} t)".format(bus, source)]
        vn_question_procedural_txt = "(PRINT t {})".format("".join(vn_question_procedural))

    with open('Output/output_c.txt', 'w') as writer:
        writer.writelines("+ Procedural Form: {}\n".format(vn_question_procedural_txt))


################### d. Trả lời câu truy vấn ############################################################################

# Check the question type
ans = None
if "PRINT b" in vn_question_procedural_txt:
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

elif "RUN-TIME" in vn_question_procedural_txt:
    procedure, bus, source, dest, time = vn_question_procedural.split(" ")
    procedure, time = procedure.replace("(", ""), time.replace(")", "")
    ans = None
    for data in database[procedure]:
        data_bus, data_source, data_dest, data_time = data.split(" ")
        if bus == data_bus and source == data_source and dest == data_dest:
            ans = data_time
elif "PRINT t" in vn_question_procedural_txt:
    ans_lst = {}
    parsed_data = vn_question_procedural[1].split(" ")
    procedure, bus, loc, time = parsed_data[0].replace("(", ""), parsed_data[1], parsed_data[2], parsed_data[3].replace(")", "")
    for data in database[procedure]:
        data_bus, data_loc, data_time = data.split(" ")
        if data_bus == bus and data_loc == loc:
            ans_lst[data_bus] = data_time

    ans = []
    for item in ans_lst.items():
        if item[0] in database["BUS"]:
            ans.append(item[1])

else:
    exit("The type of question has not handled yet!")

with open('Output/output_d.txt', 'w') as writer:
    writer.writelines("+ Answer: {}\n".format(ans if ans else None))
