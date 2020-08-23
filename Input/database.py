# all lowercase. structure: word: (word-type, semantic)
vn_dictionary = {
    # add for question: Xe bus nào đi đến thành phố Huế lúc 20:00HR ?
    "xe bus": ("N", "BUS"),
    "nào": ("WH", "NÀO"),
    "đi": ("V", "ĐI"),
    "đến": ("P", "ĐẾN"),
    "thành phố huế": ("CITY", "HUE"),
    "lúc": ("P", "LÚC"),
    "20:00hr": ("TIME", "20:00HR"),

    # add for question: Thời gian nào xe bus B3 đi từ Đà Nẵng đến Huế ?
    "thời gian": ("TIME", "TIME"),
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
    "RUN-TIME": {
        "B1 HCMC HUE 12:00HR",
        "B2 HCMC HUE 10:00HR",
        "B3 DANANG HCMC 14:00HR",
        "B4 HCMC DANANG 12:00HR",
        "B5 DANANG HUE 5:00HR",
        "B6 DANANG HUE 4:00HR",
        "B7 HCMC HUE 12:00HR",
    },
}