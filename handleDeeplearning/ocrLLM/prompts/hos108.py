prompt = """lưu ý không sử dụng kiến thức cá nhân để trả lời câu hỏi mà phải dựa vào nội dung context: {context}
              . hãy truy xuất thông tin các thông tin sau :
              - MS(mẫu số)
              - so_ben_an(số bệnh án)
              - ma_so_nguoi_benh(mã số người bệnh)
              - Ho_ten(họ và tên người bệnh)
              - ngay_sinh(ngày sinh)
              - Gioi_tinh(giới tính)
              - Dia_chi(địa chỉ)
              - khoa_dieu_tri(khoa điều trị)
              - vao_vien_luc(vào viện lúc)
              - ra_vien_luc(ra viện lúc)
              - tong_ngay_dieu_tri(tổng ngày điều trị)
              - chan_doan_khi_ra_vien(chẩn đoán khi ra viện)
              - ma_benh(mã bệnh)
              - benh_kem_theo(bệnh kèm theo)
              - so_tien_bang_chu(số tiền bằng chữ)
              - total_expenses(tổng chi phí khám bệnh, chữa bệnh)
              - mien_giam(số tiền miễn giảm (Voucher))
              - tong_chi_tra(Tổng số tiền chi trả lại)
              - tong_bn_chi_tra(Tổng số tiền bệnh nhân chi trả)
              - so_tien_tam_gui(số tiền tạm gửi)
              - nguon_khac(nguồn khác)
              - (chi phí còn lại)
              - tien_thua(thừa)
              - tien_thieu(thiếu)

              ví dụ của cấu trúc json là:
                {{
                    "MS": "mẫu số",
                    "so_ben_an": "số bệnh án",
                    "ma_so_nguoi_benh": "mã số người bệnh",
                    "Ho_ten": "họ và tên người bệnh",
                    "ngay_sinh": "ngày sinh",
                    "Gioi_tinh": "giới tính",
                    "Dia_chi": "địa chỉ",
                    "khoa_dieu_tri": "khoa điều trị",
                    "vao_vien_luc": "vào viện lúc",
                    "ra_vien_luc": "ra viện lúc",
                    "tong_ngay_dieu_tri": "tổng ngày điều trị",
                    "chan_doan_khi_ra_vien": "chẩn đoán khi ra viện",
                    "ma_benh": "mã bệnh",
                    "benh_kem_theo": "bệnh kèm theo",
                    "so_tien_bang_chu": "số tiền bằng chữ",
                    "total_expenses": "tổng chi phí khám bệnh, chữa bệnh",
                    "mien_giam": "số tiền miễn giảm (Voucher)",
                    "tong_chi_tra": "Tổng số tiền chi trả lại",
                    "tong_bn_chi_tra": "Tổng số tiền bệnh nhân chi trả",
                    "so_tien_tam_gui": "số tiền tạm gửi",
                    "nguon_khac": "nguồn khác",
                    "chi_phi_con_lai": "chi phí còn lại",
                    "tien_thua": "thừa",
                    "tien_thieu": "thiếu"
                }}
      """