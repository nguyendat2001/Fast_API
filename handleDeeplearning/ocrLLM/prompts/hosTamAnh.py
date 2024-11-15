prompt = """lưu ý không sử dụng kiến thức cá nhân để trả lời câu hỏi mà phải dựa vào nội dung context: {context}
              . hãy truy xuất thông tin các thông tin sau :
              - MS(mã)
              - so_hieu(số hiệu)
              - ma_so(mã số)
              - so_bien_lai(số biên lai)
              - lan_in_thu(lần in thứ)
              - Ho_ten(họ và tên bệnh nhân)
              - Nam_sinh(năm sinh)
              - Gioi_tinh(giới tính)
              - Dia_chi(địa chỉ)
              - ten_cty(tên công ty)
              - ma_thue(mã số thuế)
              - BHYT:{{
                  from(giá trị từ):
                  to(đến ngày):
                  ma_the(mã thẻ):
              }}
              - noi_dk(nơi đăng ký BHYT lúc ban đầu):
              - Khoa_phong (khoa phòng)
              - Thoi_gian_vao_vien(thời gian vào viện)
              - tong_chi_phi(tổng chi phí)
              - BHYT_chi_tra (BHYT chi trả)
              - niem_giam(Miễn giảm)
              - benh_nhan_chi_tra(Bệnh nhân chi trả)
              - benh_nhan_da_tam_ung(Bệnh nhân đã tạm ứng)
              - BHYT_chi_tra (BHYT chi trả)
              - BN_chi_tra_them(Bệnh nhân phải chi trả thêm (4)-(5):)
              - BN_duoc_hoan_lai(Bệnh nhân được hoàn lại)

              ví dụ của cấu trúc json là:
                {{
                    "MS": "mã",
                    "so_hieu": "số hiệu",
                    "ma_so": "mã số",
                    "so_bien_lai": "số biên lai",
                    "lan_in_thu": "lần in thứ",
                    "Ho_ten": "họ và tên bệnh nhân",
                    "Nam_sinh": "năm sinh",
                    "Gioi_tinh": "giới tính",
                    "Dia_chi": "địa chỉ",
                    "ten_cty": "tên công ty",
                    "ma_thue": "mã số thuế",
                    "BHYT": {{
                        "from"("giá trị từ"): ,
                        "to"("đến ngày"): ,
                        "ma_the"("mã thẻ"):
                    }},
                    "noi_dk"("nơi đăng ký BHYT lúc ban đầu"): ,
                    "Khoa_phong": "khoa phòng",
                    "Thoi_gian_vao_vien": "thời gian vào viện",
                    "tong_chi_phi": "tổng chi phí",
                    "BHYT_chi_tra": "BHYT chi trả",
                    "niem_giam": "Miễn giảm",
                    "benh_nhan_chi_tra": "Bệnh nhân chi trả",
                    "benh_nhan_da_tam_ung": "Bệnh nhân đã tạm ứng",
                    "BN_chi_tra_them": "Bệnh nhân phải chi trả thêm",
                    "BN_duoc_hoan_lai": "Bệnh nhân được hoàn lại"
                }}
      """