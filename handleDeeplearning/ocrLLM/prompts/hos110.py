prompt = """Lưu ý: Không sử dụng kiến thức cá nhân để trả lời câu hỏi. Câu trả lời phải dựa hoàn toàn vào nội dung trong đoạn *context* dưới đây:

Context:
{context}

Yêu cầu:
Hãy truy xuất các thông tin sau từ *context*. Nếu trường nào không có thông tin, hãy đặt giá trị là `null`, không để `[redacted]`.

Danh sách các thông tin cần truy xuất:
- MS (mẫu số)
- ma_so_nguoi_benh (mã số người bệnh)
- so_kham_benh (số khám bệnh)
- ma_benh_an (mã bệnh án)
- Ho_ten (họ tên người bệnh)
- ngay_sinh (ngày tháng năm sinh)
- Gioi_tinh (giới tính)
- Dia_chi (địa chỉ hiện tại)
- ma_khu_vuc (mã khu vực thuộc: K1/K2/K3 hoặc null)
- ma_the_BHYT (mã thẻ BHYT)
- from_BHYT (giá trị từ ngày của BHYT)
- to_BHYT (giá trị đến ngày của BHYT)
- doi_tuong_KCB (đối tượng KCB)
- noi_DK_KCB (nơi ĐK KCB ban đầu)
- ma (mã)
- den_kham (đến khám)
- dieu_tri_tu (điều trị ngoại trú/nội trú từ)
- ket_thuc (kết thúc khám/điều trị)
- tong_ngay_dieu_tri (tổng số ngày điều trị)
- tinh_trang_ra_vien (tình trạng ra viện)
- cap_cuu (cấp cứu)
- dung_tuyen (đúng tuyến)
- thong_tuyen (thông tuyến)
- trai_tuyen (trái tuyến)
- noi_chuyen_den_tu (nơi chuyển đến từ)
- noi_chuyen_di (nơi chuyển đi)
- chan_doan_xac_dinh (chẩn đoán xác định)
- ma_benh (mã bệnh)
- benh_kem_theo (bệnh kèm theo)
- ma_benh_kem_theo (mã bệnh kèm theo)
- thoi_diem_du_5_nam_tu_ngay (thời điểm đủ 5 năm liên tục từ ngày)
- mien_cung_chi_tra_trong_nam_tu_ngay (miễn cùng chi trả trong năm từ ngày)
- ma_BHYT (mã thẻ BHYT)
- gia_tri_tu (giá trị từ ngày của BHYT)
- gia_tri_den (giá trị đến ngày của BHYT)
- muc_huong (mức hưởng của BHYT)
- treament_expenses (chi phí khám chữa bệnh cho cả đợt điều trị, làm tròn đến đơn vị đồng)
- treament_expenses_word (chi phí khám chữa bệnh viết bằng chữ)
- BHYT_thanh_toan (quỹ BHYT thanh toán)
- nguoi_benh_tra (số tiền người bệnh trả, trong đó:)
  - tra_trong_pv_BHYT (số tiền cùng trả trong phạm vi BHYT)
  - khoan_tra_khac (các khoản phải trả khác)
  - nguon_khac (nguồn khác)
- tam_thu (tạm thu)
- so_tien_NB_thanh_toan (số tiền người bệnh phải thanh toán)
- so_tien_can_thu_them (số tiền cần thu thêm)
- so_tien_con_lai (số tiền còn lại)

Yêu cầu đầu ra:
Hãy trả về dữ liệu trong định dạng JSON. Nếu không có thông tin, hãy điền `null` vào trường tương ứng.

Ví dụ về cấu trúc JSON hợp lệ:
```json
{{
    "MS": "mẫu số",
    "ma_so_nguoi_benh": "mã số người bệnh",
    "so_kham_benh": "số khám bệnh",
    "ma_benh_an": "mã bệnh án",
    "Ho_ten": "họ và tên người bệnh",
    "ngay_sinh": "ngày tháng năm sinh",
    "Gioi_tinh": "giới tính",
    "Dia_chi": "địa chỉ",
    "ma_khu_vuc": "mã khu vực thuộc: K1/K2/K3 hoặc null",
    "ma_the_BHYT": "mã thẻ BHYT",
    "from_BHYT": "giá trị từ ngày của BHYT",
    "to_BHYT": "giá trị đến ngày của BHYT",
    "doi_tuong_KCB": "đối tượng KCB",
    "noi_DK_KCB": "nơi ĐK KCB ban đầu",
    "ma": "mã",
    "den_kham": "đến khám",
    "dieu_tri_tu": "điều trị ngoại trú/nội trú từ",
    "ket_thuc": "kết thúc khám/điều trị",
    "tong_ngay_dieu_tri": "tổng số ngày điều trị",
    "tinh_trang_ra_vien": "tình trạng ra viện",
    "cap_cuu": "cấp cứu",
    "dung_tuyen": "đúng tuyến",
    "thong_tuyen": "thông tuyến",
    "trai_tuyen": "trái tuyến",
    "noi_chuyen_den_tu": "nơi chuyển đến từ",
    "noi_chuyen_di": "nơi chuyển đi",
    "chan_doan_xac_dinh": "chẩn đoán xác định",
    "ma_benh": "mã bệnh",
    "benh_kem_theo": "bệnh kèm theo",
    "ma_benh_kem_theo": "mã bệnh kèm theo",
    "thoi_diem_du_5_nam_tu_ngay": "thời điểm đủ 5 năm liên tục từ ngày",
    "mien_cung_chi_tra_trong_nam_tu_ngay": "miễn cùng chi trả trong năm từ ngày",
    "ma_BHYT": "mã thẻ BHYT",
    "gia_tri_tu": "giá trị từ ngày của BHYT",
    "gia_tri_den": "giá trị đến ngày của BHYT",
    "muc_huong": "mức hưởng của BHYT",
    "treament_expenses": "chi phí khám chữa bệnh cho cả đợt điều trị, làm tròn đến đơn vị đồng",
    "treament_expenses_word": "chi phí khám chữa bệnh viết bằng chữ",
    "BHYT_thanh_toan": "quỹ BHYT thanh toán",
    "nguoi_benh_tra": "số tiền người bệnh trả, trong đó:",
    "tra_trong_pv_BHYT": "số tiền cùng trả trong phạm vi BHYT",
    "khoan_tra_khac": "các khoản phải trả khác",
    "nguon_khac": "nguồn khác",
    "tam_thu": "tạm thu",
    "so_tien_NB_thanh_toan": "số tiền người bệnh phải thanh toán",
    "so_tien_can_thu_them": "số tiền cần thu thêm",
    "so_tien_con_lai": "số tiền còn lại"
}}
```
"""


header_prompt = """Lưu ý: Không sử dụng kiến thức cá nhân để trả lời câu hỏi. Câu trả lời phải dựa hoàn toàn vào nội dung trong đoạn *context* dưới đây:

Context:
{context}

Yêu cầu:
Hãy truy xuất các thông tin sau từ *context*. Nếu trường nào không có thông tin, hãy đặt giá trị là `null`, không để `[redacted]`.

Danh sách các thông tin cần truy xuất:
- MS (mẫu số)
- ma_so_nguoi_benh (mã số người bệnh)
- so_kham_benh (số khám bệnh)
- ma_benh_an (mã bệnh án)
Yêu cầu đầu ra:
Hãy trả về dữ liệu trong định dạng JSON. Nếu không có thông tin, hãy điền `null` vào trường tương ứng.

Ví dụ về cấu trúc JSON hợp lệ:
```json
{{
    "MS": "mẫu số",
    "ma_so_nguoi_benh": "mã số người bệnh",
    "so_kham_benh": "số khám bệnh",
    "ma_benh_an": "mã bệnh án"
}}
```
"""

sub_header_prompt = """Lưu ý: Không sử dụng kiến thức cá nhân để trả lời câu hỏi. Câu trả lời phải dựa hoàn toàn vào nội dung trong đoạn *context* dưới đây:

Context:
{context}

Yêu cầu:
Hãy truy xuất các thông tin sau từ *context*. Nếu trường nào không có thông tin, hãy đặt giá trị là `null`, không để `[redacted]`.

Danh sách các thông tin cần truy xuất:
- Ho_ten_nguoi_benh (họ tên người bệnh)
- ngay_sinh (ngày tháng năm sinh)
- Gioi_tinh (giới tính)
- Dia_chi (địa chỉ hiện tại)
- ma_khu_vuc (mã khu vực thuộc: K1/K2/K3 hoặc null)
- ma_the_BHYT (mã thẻ BHYT)
- from_BHYT (giá trị từ ngày của BHYT)
- to_BHYT (giá trị đến ngày của BHYT)
- doi_tuong_KCB (đối tượng KCB)
- noi_DK_KCB (nơi ĐK KCB ban đầu)
- ma (mã)
- den_kham (đến khám "format: _ giờ _ phút, ngày _ Ví dụ: 08 giờ 55 phút, ngày 27/05/2022")
- dieu_tri_tu (điều trị ngoại trú/nội trú từ "format: _ giờ _ phút, ngày _ Ví dụ: 08 giờ 55 phút, ngày 27/05/2022")
- ket_thuc (kết thúc khám/điều trị "format: _ giờ _ phút, ngày _ Ví dụ: 08 giờ 55 phút, ngày 27/05/2022")
- tong_ngay_dieu_tri (tổng số ngày điều trị)
- tinh_trang_ra_vien (tình trạng ra viện)
- cap_cuu (cấp cứu)
- dung_tuyen (đúng tuyến)
- thong_tuyen (thông tuyến)
- trai_tuyen (trái tuyến)
- noi_chuyen_den_tu (nơi chuyển đến từ)
- noi_chuyen_di (nơi chuyển đi)
- chan_doan_xac_dinh (chẩn đoán xác định)
- ma_benh (mã bệnh)
- benh_kem_theo (bệnh kèm theo)
- ma_benh_kem_theo (mã bệnh kèm theo)
- thoi_diem_du_5_nam_tu_ngay (thời điểm đủ 5 năm liên tục từ ngày)
- mien_cung_chi_tra_trong_nam_tu_ngay (miễn cùng chi trả trong năm từ ngày)
- ma_BHYT (mã thẻ BHYT)
- gia_tri_tu (giá trị từ ngày của BHYT)
- gia_tri_den (giá trị đến ngày của BHYT)
- muc_huong (mức hưởng của BHYT)
Yêu cầu đầu ra:
Hãy trả về dữ liệu trong định dạng JSON. Nếu không có thông tin, hãy điền `null` vào trường tương ứng.

Ví dụ về cấu trúc JSON hợp lệ:
```json
{{
    "Ho_ten_nguoi_benh": "nguyễn văn a",
    "ngay_sinh": "20/09/2011,
    "Gioi_tinh": "nam",
    "Dia_chi": "Ninh Sơn, Việt Yên, Bắc Giang, Việt Nam",
    "ma_khu_vuc": null,
    "ma_the_BHYT": "9320814878",
    "from_BHYT": "01/01/2022",
    "to_BHYT": "01/01/2022",
    "doi_tuong_KCB": "Bảo hiểm y tế",
    "noi_DK_KCB": "Trạm y tế Xã Ninh Sơn",
    "ma": "31222",
    "den_kham": "08 giờ 55 phút, ngày 27/05/2022",
    "dieu_tri_tu": "08 giờ 55 phút, ngày 27/05/2022",
    "ket_thuc": "08 giờ 55 phút, ngày 27/05/2022",
    "tong_ngay_dieu_tri": "6",
    "tinh_trang_ra_vien": "1",
    "cap_cuu": null,
    "dung_tuyen": null,
    "thong_tuyen": null,
    "trai_tuyen": null,
    "noi_chuyen_den_tu": "nơi chuyển đến từ",
    "noi_chuyen_di": "nơi chuyển đi",
    "chan_doan_xac_dinh": "chẩn đoán xác định",
    "ma_benh": "mã bệnh",
    "benh_kem_theo": "bệnh kèm theo",
    "ma_benh_kem_theo": "mã bệnh kèm theo",
    "thoi_diem_du_5_nam_tu_ngay": "thời điểm đủ 5 năm liên tục từ ngày",
    "mien_cung_chi_tra_trong_nam_tu_ngay": "miễn cùng chi trả trong năm từ ngày",
    "ma_BHYT": "9320814878",
    "gia_tri_tu": "01/01/2022",
    "gia_tri_den": "01/01/2022",
    "muc_huong": "80"
}}
```
"""


sumary_prompt = """Lưu ý: Không sử dụng kiến thức cá nhân để trả lời câu hỏi. Câu trả lời phải dựa hoàn toàn vào nội dung trong đoạn *context* dưới đây:

Context:
{context}

Yêu cầu:
Hãy truy xuất các thông tin sau từ *context*. Nếu trường nào không có thông tin, hãy đặt giá trị là `null`, không để `[redacted]`.

Danh sách các thông tin cần truy xuất:
- treament_expenses (chi phí lần khám bệnh/cả đợt điều trị(làm tròn đến đơn vị đồng): "ví dụ: 5.123.421")
- treament_expenses_word (chi phí khám chữa bệnh viết bằng chữ)
- BHYT_thanh_toan (quỹ BHYT thanh toán)
- nguoi_benh_tra (số tiền người bệnh trả, trong đó:)
- tra_trong_pv_BHYT (số tiền cùng trả trong phạm vi BHYT)
- khoan_tra_khac (các khoản phải trả khác)
- nguon_khac (nguồn khác)
- tam_thu (tạm thu)
- so_tien_NB_thanh_toan (số tiền người bệnh phải thanh toán)
- so_tien_can_thu_them (số tiền cần thu thêm)
- so_tien_con_lai (số tiền còn lại)

Yêu cầu đầu ra:
Hãy trả về dữ liệu trong định dạng JSON. Nếu không có thông tin, hãy điền `null` vào trường tương ứng.

Ví dụ về cấu trúc JSON hợp lệ:
```json
{{
    "treament_expenses": "5.123.421",
    "treament_expenses_word": "chi phí khám chữa bệnh viết bằng chữ",
    "BHYT_thanh_toan": ""5.123.421",
    "nguoi_benh_tra": ""5.123.421",
    "tra_trong_pv_BHYT": ""5.123.421",
    "khoan_tra_khac": ""5.123.421",
    "nguon_khac": ""5.123.421",
    "tam_thu": ""5.123.421",
    "so_tien_NB_thanh_toan": ""5.123.421",
    "so_tien_can_thu_them": ""5.123.421",
    "so_tien_con_lai": ""5.123.421"
}}
```
"""