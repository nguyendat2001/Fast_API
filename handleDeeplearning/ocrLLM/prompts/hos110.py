prompt = """lưu ý không sử dụng kiến thức cá nhân để trả lời câu hỏi mà phải dựa vào nội dung context: {context}
              . hãy truy xuất thông tin các thông tin sau và trường nào không có thông tin cứ để null:
              - MS(mẫu số)
              - ma_so_nguoi_benh(mã số người bệnh)
              - so_kham_benh(số khám bệnh)
              - ma_benh_an(mã bệnh án)
              - Ho_ten((1)họ tên người bệnh)
              - ngay_sinh(ngày tháng năm sinh)
              - Gioi_tinh(giới tính)
              - Dia_chi((2)địa chỉ hiện tại)
              - ma_khu_vuc((3)mã khu vực(K1/K2/K3))
              - ma_the_BHYT((4)mã thẻ BHYT)
              - from_BHYT(giá trị từ ngày của BHYT)
              - to_BHYT(giá trị đến ngày của BHYT)
              - doi_tuong_KCB(đối tượng KCB)
              - noi_DK_KCB((5)nơi ĐK KCB ban đầu)
              - ma((6) mã)
              - den_kham((7) đến khám)
              - dieu_tri_tu((8) điều trị ngoại trú/ nội trú từ)
              - ket_thuc((9) kết thúc khám/ điều trị)
              - tong_ngay_dieu_tri(tổng số ngày điều trị)
              - tinh_trang_ra_vien((10) tình trạng ra viện)
              - cap_cuu((11) cấp cứu)
              - dung_tuyen((12) đúng tuyến)
              - thong_tuyen((13) thông tuyến)
              - trai_tuyen((14) trái tuyến)
              - noi_chuyen_den_tu(nơi chuyến đến từ)
              - noi_chuyen_di(nơi chuyến đi)
              - chan_doan_xac_dinh((15)chẩn đoán xác định)
              - ma_benh((16)mã bệnh)
              - benh_kem_theo((17)bệnh kèm theo)
              - ma_benh_kem_theo((18)mã bệnh kèm theo)
              - thoi_diem_du_5_nam_tu_ngay((19)thời điểm đủ 5 năm liên tục từ ngày)
              - mien_cung_chi_tra_trong_nam_tu_ngay((20)miễn cùng chi trả trong năm từ ngày)
              - ma_BHYT(mã thẻ BHYT)
              - gia_tri_tu(giá trị từ ngày của BHYT)
              - gia_tri_den(giá đến ngày của BHYT)
              - muc_huong(mức hưởng của BHYT)

              - treament_expenses(chi phí khám chửa bệnh cho cả đợt điều trị(làm tròn đến đơn vị đồng))
              - treament_expenses_word(chi phí khám chửa bệnh viết bằng chữ)
              - BHYT_thanh_toan(quỹ BHYT thanh toán)
              - nguoi_benh_tra(số tiền người bệnh trả, trong đó)
              - tra_trong_pv_BHYT(số tiền cùng trả trong phạm vi BHYT)
              - khoan_tra_khac(các khoản phải trả khác)
              - nguon_khac(nguồn khác)
              - tam_thu(tạm thu)
              - so_tien_NB_thanh_toan(số tiền NB phải thanh toán)
              - so_tien_can_thu_them(số tiền cần thu thêm)
              - so_tien_con_lai(số tiền còn lại)

              ví dụ của cấu trúc json là:
                {{
                    "MS": "mẫu số",
                    "ma_so_nguoi_benh": "mã số người bệnh",
                    "so_kham_benh": (số khám bệnh),
                    "so_ben_an": "số bệnh án",
                    "Ho_ten": "họ và tên người bệnh",
                    "ngay_sinh": "ngày tháng năm sinh",
                    "Gioi_tinh": "giới tính",
                    "Dia_chi": "địa chỉ",
                    "ma_khu_vuc": "mã khu vực(K1/K2/K3)",
                    "ma_the_BHYT": "mã thẻ BHYT",
                    "from_BHYT": "giá trị từ ngày của BHYT",
                    "to_BHYT": "giá trị đến ngày của BHYT",
                    "doi_tuong_KCB": "đối tượng KCB",
                    "noi_DK_KCB": "nơi ĐK KCB ban đầu",
                    "ma": "mã",
                    "den_kham": "đến khám",
                    "dieu_tri_tu": "điều trị ngoại trú/ nội trú từ",
                    "ket_thuc": "kết thúc khám/ điều trị",
                    "tong_ngay_dieu_tri": "tổng số ngày điều trị",
                    "tinh_trang_ra_vien": "tình trạng ra viện",
                    "cap_cuu": "cấp cứu",
                    "dung_tuyen": "đúng tuyến",
                    "trai_tuyen": "trái tuyến",
                    "thong_tuyen": "thông tuyến",
                    "noi_chuyen_den_tu": "nơi chuyến đến từ",
                    "noi_chuyen_di": "nơi chuyến đi",
                    "chan_doan_xac_dinh": "chẩn đoán xác định",
                    "ma_benh": "mã bệnh",
                    "benh_kem_theo": "bệnh kèm theo",
                    "ma_benh_kem_theo": "mã bệnh kèm theo",
                    "thoi_diem_du_5_nam_tu_ngay": "thời điểm đủ 5 năm liên tục từ ngày",
                    "mien_cung_chi_tra_trong_nam_tu_ngay": "miễn cùng chi trả trong năm từ ngày",
                    "ma_BHYT": "mã thẻ BHYT",
                    "gia_tri_tu": "giá trị từ ngày của BHYT",
                    "gia_tri_den": "giá đến ngày của BHYT",
                    "muc_huong": "mức hưởng của BHYT",
                    "treament_expenses": "chi phí khám chửa bệnh cho cả đợt điều trị(làm tròn đến đơn vị đồng)",
                    "treament_expenses_word": "chi phí khám chửa bệnh viết bằng chữ",
                    "BHYT_thanh_toan": "quỹ BHYT thanh toán",
                    "nguoi_benh_tra": "số tiền người bệnh trả, trong đó",
                    "tra_trong_pv_BHYT": "số tiền cùng trả trong phạm vi BHYT",
                    "khoan_tra_khac": "các khoản phải trả khác",
                    "nguon_khac": "nguồn khác",
                    "tam_thu": "tạm thu",
                    "so_tien_NB_thanh_toan": "số tiền NB phải thanh toán",
                    "so_tien_can_thu_them": "số tiền cần thu thêm",
                    "so_tien_con_lai": "số tiền còn lại"
                }}
      """