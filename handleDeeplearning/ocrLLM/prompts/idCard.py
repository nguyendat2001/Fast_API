prompt = """lưu ý không sử dụng kiến thức cá nhân để trả lời câu hỏi mà phải dựa vào nội dung context: {context}
              . hãy truy xuất thông tin các thông tin sau :
              - id_number(mã số)
              - name(họ và tên)
              - date_of_birth(ngày tháng năm sinh)
              - gender(giới tính)
              - nation(quốc tịch)
              - province(quê quán)
              - president_address(nơi thường trú)

              ví dụ của cấu trúc json là:
                {{
                    "id_number": "mã số",
                    "name": "họ và tên",
                    "date_of_birth": "ngày tháng năm sinh",
                    "gender": "giới tính",
                    "nation": "quốc tịch",
                    "province": "quê quán",
                    "president_address": "nơi thường trú"
                }}
      """