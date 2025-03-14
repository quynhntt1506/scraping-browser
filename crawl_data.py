from lxml.html.clean import clean_html
from lxml import html
import json

class ElementInfo:
    def __init__(self, class_name, type, content, href):
        self.class_name = class_name
        self.type = type
        self.content = content
        self.href = href

def get_data_to_table (output_data):
    # Chuyển dữ liệu thành bảng HTML
    table_rows = ""
    for section, items in output_data.items():
        first_row = True  # Đánh dấu hàng đầu tiên của mỗi section
        rowspan = len(items)  # Số hàng cần merge

        for index, item in enumerate(items):
            links_html = "<br>".join([f"<a href='{link}' target='_blank'>{link}</a>" for link in item.get("links", [])])

            # Nếu là dòng đầu tiên, dùng rowspan
            section_html = f"<td style='padding: 5px;' rowspan='{rowspan}'>{section}</td>" if index == 0 else ""

            table_rows += f"""
            <tr>
                {section_html}
                <td style="padding: 5px;">{item.get("content", "")}</td>
                <td style="padding: 5px;">{links_html}</td>
            </tr>
            """


    popup_script = f"""
    let popup = document.createElement('div');
    popup.style.position = 'fixed';
    popup.style.top = '50%';
    popup.style.left = '50%';
    popup.style.transform = 'translate(-50%, -50%)';
    popup.style.background = 'white';
    popup.style.padding = '20px';
    popup.style.boxShadow = '0px 0px 10px rgba(0, 0, 0, 0.2)';
    popup.style.borderRadius = '10px';
    popup.style.zIndex = '10000';
    popup.style.width = '60vw';
    popup.style.maxWidth = '1500px';
    popup.style.fontFamily = 'Arial, sans-serif';
    popup.innerHTML = `
        <h2 style="text-align:center; margin-bottom: 15px; color: #333;">Kết quả phân tích dữ liệu</h2>
        <div style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 5px;">
            <table border="1" cellspacing="0" cellpadding="8" style="width:100%; border-collapse:collapse; text-align:left; font-size: 14px;">
                <thead style="position: sticky; top: 0; background: white; z-index: 10;">
                    <tr style="background: #CCCCCC;">
                        <th style="padding: 5px;">Key</th>
                        <th style="padding: 5px;">Content</th>
                        <th style="padding: 5px;">Link</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
        <br>
        <button onclick="this.parentElement.remove()" 
            style="display:block; margin:auto; padding:10px 20px; font-size: 14px; color: white; background: #dc3545; border: none; border-radius: 5px; cursor: pointer;">
            Đóng
        </button>
    `;
    document.body.appendChild(popup);
    """
    return popup_script

def scraping_data (driver, htmls):
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
                    sections.append(ElementInfo(class_name, "link", text, href))

            elif tag == "picture" or tag == "img" or tag == 'svg':  # Nếu là thẻ <img>
                sources = ""
                alt = ""
                if tag == "picture":
                    img = elem.find(".//img")
                    sources = next((source.get("srcset") for source in elem.xpath(".//source") if source.get("srcset")), None) or img.get("src") if img is not None else ""
                else:
                    sources = elem.get("src", "").strip()
                    alt = elem.get("alt", "").strip()
                if sources:
                    sections.append(ElementInfo(class_name, "image", alt, sources))

            else:  # Các thẻ khác
                text_content = (elem.text or "").strip()
                if text_content != "":
                    sections.append(ElementInfo(class_name, "text", text_content, ''))

        # Ghi vào file JSON
        json_data = [
            {
                "class_name": element.class_name,
                "type": element.type,
                "content": element.content,
                "link": element.href
            }
            for element in sections
        ]
        output_data.update({f"section_{index}": json_data})

    # Lọc bỏ nội dung trùng lặp trong mỗi section
    # ============
    filtered_data = {}
    for section, items in output_data.items():
        grouped_content = {}  # Dùng dictionary để gom nhóm theo content

        for item in items:
            content = item.get("content", "")
            link = item.get("link", "")

            if content in grouped_content:
                if link and link not in grouped_content[content]["links"]:
                    grouped_content[content]["links"].append(link)  # Chỉ thêm link nếu chưa tồn tại
            else:
                grouped_content[content] = {
                    "class_name": item.get("class_name", ""),
                    "type": item.get("type", ""),
                    "content": content,
                    "links": [link] if link else [],  # Khởi tạo mảng link
                }

        filtered_data[section] = list(grouped_content.values())
    driver.execute_script(get_data_to_table(filtered_data))
    # ============
    print(output_data)
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)

    print("Đã lưu dữ liệu vào output_test.json 🎯")






