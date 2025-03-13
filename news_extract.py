from lxml.html.clean import clean_html
from lxml import html
import json

# Giả sử html_content đã được lấy từ một trang web
def scraping_data (htmls):
    output_data = {}
    index = 0
    for html_path in htmls:
        index = index + 1
        tree = html.fromstring(html_path)
        # Danh sách chứa các object con trong sections
        sections = []

        # Hàm tìm class gần nhất
        def get_nearest_class(elem):
            while elem is not None:
                class_name = elem.get("class")
                if class_name:  # Nếu tìm thấy class, trả về ngay
                    return class_name
                elem = elem.getparent()  # Di chuyển lên thẻ cha
            return "no-class"  # Nếu không có class nào

        for elem in tree.xpath("//*"):
            tag = elem.tag  # Loại thẻ (p, div, a, img, picture, ...)
            class_name = elem.get("class") or get_nearest_class(elem)  # Lấy class gần nhất

            if tag == "a":  # Nếu là thẻ <a>
                href = elem.get("href", "").strip()
                text = (elem.text or "").strip()
                if href and text:
                    sections.append({
                        "class-name": class_name,
                        "type": "link",
                        "text": text,
                        "href": href
                    })

            # elif tag == "img" or tag == 'svg':  # Nếu là thẻ <img>
            #     src = elem.get("src", "").strip()
            #     alt = elem.get("alt", "").strip()
            #     if src:
            #         sections.append({
            #             "class-name": class_name,
            #             "type": "image",
            #             "src": src,
            #             "alt": alt
            #         })

            elif tag == "picture" or tag == "img" or tag == 'svg':  # Nếu là thẻ <picture>
                sources = ""
                alt = ""
                if tag == "picture":
                    img = elem.find(".//img")
                    sources = next((source.get("srcset") for source in elem.xpath(".//source") if source.get("srcset")), None) or img.get("src") if img is not None else ""
                else:
                    sources = elem.get("src", "").strip()
                    alt = elem.get("alt", "").strip()
                    
                # sources = [source.get("srcset") for source in elem.xpath(".//source") if source.get("srcset")]
                # img = elem.find(".//img")
                # img_src = img.get("src") if img is not None else ""
                if sources:
                    sections.append({
                        "class-name": class_name,
                        "type": "image",
                        "sources": sources,
                        "alt": alt
                    })

            else:  # Các thẻ khác
                text_content = (elem.text or "").strip()
                if text_content:
                    sections.append({
                        "class-name": class_name,
                        "type": "text",
                        "content": text_content
                    })
        # Loại bỏ các object có class-name trùng lặp
        unique_class_names = set()
        filtered_sections = []

        for obj in sections:
            class_name = obj["class-name"]
            if class_name not in unique_class_names:
                unique_class_names.add(class_name)
                filtered_sections.append(obj)
                
                
        # Ghi vào file JSON
        output_data.update({f"sections_{index}": filtered_sections})

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print("Đã lưu dữ liệu vào output-one-element.json 🎯")



# def extract_html_data(html_tags):
#     """ Trích xuất thông tin từ danh sách thẻ HTML và hiển thị dưới dạng bảng """
#     data = []
    
#     for html in html_tags:
#         soup = BeautifulSoup(html, "html.parser")
#         element = soup.find()  # Lấy thẻ đầu tiên trong chuỗi HTML
        
#         if element:
#             tag_name = element.name
#             class_name = " ".join(element.get("class", []))  # Lấy class nếu có
#             text = element.get_text(strip=True)  # Lấy nội dung text
            
#             data.append({"tag_name": tag_name, "class_name": class_name, "text": text})
    
#     df = pd.DataFrame(data)
#     return df

# # Ví dụ 3 thẻ HTML đầu vào
# html_tags = [
#     '<p class="highlight-border">Bayer Leverkusen, <a href="https://vietnamnet.vn/bayern-munich-tag2357987485850534144.html" target="_blank"><strong>Bayern Munich</strong></a> cuối cùng cũng đánh bại được đội bóng do Xabi Alonso dẫn dắt ở thời điểm quan trọng - lượt đi vòng 16 đội <a href="https://vietnamnet.vn/champions-league-tag13336189034300601840.html"><strong>Champions League</strong></a>.</p>',
#     '<p class="highlight-border">Chỉ hơn 2 tuần sau khi may mắn thoát thua Leverkusen tại BayArena, lần này CLB xứ Bavaria mang hình ảnh khác.</p>',
#     '<p class="highlight-border"><em>“Đây là bước tiến lớn đúng hướng. Tất cả mọi người đều biết gần đây chúng tôi gặp rất nhiều khó khăn khi đối đầu với Leverkusen. Họ là đội bóng thật sự rất mạnh”</em>, Harry Kane chia sẻ về chiến thắng.</p>'
# ]

# # Gọi hàm và in kết quả
# df = extract_html_data(html_tags)
# print(df)






