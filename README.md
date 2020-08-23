# BUS QUERY SYSTEM

## Input
Input bao gồm 2 file question.py và database.py

1. question.py
Chứa câu hỏi (dạng tiếng Việt) và lưu câu hỏi vào biến `vn_question`. Một số
câu hỏi ví dụ:
+ "   Xe bus nào đi đến thành phố Huế lúc 20:00HR ?   "
+ "Thời gian nào xe bus B3 đi từ Đà Nẵng đến thành phố Hồ Chí Minh ?"
+ "Thời gian nào xe bus B3 đi từ Đà Nẵng ?"
+ "Thời gian nào xe bus B3 đi đến thành phố Hồ Chí Minh ?"
+ "Xe bus nào đi đến thành phố Hồ Chí Minh ?"
+ "Những xe bus nào đi đến Huế ?"
+ "Những xe nào xuất phát từ thành phố Hồ Chí Minh ?"
+ "Những xe nào đi từ Đà nẵng đến thành phố Hồ Chí Minh ?"

2. database.py:
+ vn_dictionary: chứa từ điển, từ trong từ điển ở dạng viết thường. Một từ
trong từ điển sẽ có dạng `từ: (loại từ, ngữ nghĩa)`
+ database: chứa dữ liệu cần thiết cho truy vấn như danh sách những chuyến xe,
thời gian đến, thời gian đi, và thời gian di chuyển.

## Output
Chứa 4 file:
+ output_a.txt: chứa văn phạm phụ thuộc của câu hỏi
+ output_b.txt: chứa dạng luận lý của câu hỏi
+ output_c.txt: chứa ngữ nghĩa thủ tục của câu hỏi
+ output_d.txt: chứa câu trả lời cho câu hỏi

## main.py
Chương trình được chia làm 4 phần chính:

a. Tìm văn phạm phụ thuộc: đầu vào của phần này là câu hỏi, đầu ra là tìm văn
phạm phụ thuộc. Nguyên lý diễn dịch là Malt Parser (với stack, buffer, shift,
left arc, right arc). Sự phụ thuộc giữa các từ dựa vào từ loại của từ vựng.

b. Tìm dạng luận lý: đầu vào là văn phạm phụ thuộc, đầu ra là dạng luận lý.
Nguyên lý chính là quan hệ cú pháp (Chương 11.1, Sách Xử lý Ngôn ngữ tự nhiên,
Phan Thị Tươi)

c. Tìm ngữ nghĩa thủ tục: đầu vào là dạng luận lý, đầu ra là ngữ nghĩa thủ tục.
Nguyên lý chính Chương 12.5 Ngữ nghĩa thủ tục và hỏi đáp (Sách xử lý Ngôn ngữ
tự nhiên, Phan Thị Tươi). Các mối quan hệ: (ATIME b c t) xác định rằng xe b
đến c tại thời gian t; (DTIME b c t) xác định rằng xe b đi từ c tại thời gian t;
(RUN-TIME b s d t) xác định rằng xe b đi từ s đến d trong thời gian t.

d. Truy vấn dữ liệu và xuất kết quả: đầu vào là ngữ nghĩa thủ tục, đầu ra là
câu trả lời cho câu hỏi. Hiện tại, hiện thực hỗ trợ dạng hỏi chuyến xe bus,
hỏi thời gian xuất hành/xuất phát, và hỏi khoảng thời gian di chuyển.

## Chú thích
+ Trong tiếng Anh, từ hỏi có dạng wh. Hiện thực này xem từ "nào" như là từ hỏi
trong tiếng Việt.
+ Trong các hệ thống hỏi đáp chuyến bay (FLIGHT) và tàu hoả (TRAIN), dạng tiếng
Anh quy định động từ chính FLIGHT_V và TRAIN_V lần lượt là flight và go. Hiện
thực này xem động từ chính của bus là "đi".
+ "đến" và "từ" được xem như các giới từ. Ví dụ "đến Huế", "từ Hà Nội", ...
+ Dạng câu hỏi phải có từ hỏi ("nào") và động từ chính ("đi")
