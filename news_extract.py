from lxml.html.clean import clean_html
from lxml import html
from bs4 import BeautifulSoup
import requests
from readability import Document
import json
from collections import defaultdict


# Giả sử html_content đã được lấy từ một trang web
def scraping_data_one_element (html_content):
    tree = html.fromstring(html_content)
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

        elif tag == "img":  # Nếu là thẻ <img>
            src = elem.get("src", "").strip()
            alt = elem.get("alt", "").strip()
            if src:
                sections.append({
                    "class-name": class_name,
                    "type": "image",
                    "src": src,
                    "alt": alt
                })

        elif tag == "picture":  # Nếu là thẻ <picture>
            sources = [source.get("srcset") for source in elem.xpath(".//source") if source.get("srcset")]
            img = elem.find(".//img")
            img_src = img.get("src") if img is not None else ""
            if sources or img_src:
                sections.append({
                    "class-name": class_name,
                    "type": "picture",
                    "sources": sources,
                    "img_src": img_src
                })

        else:  # Các thẻ khác
            text_content = (elem.text or "").strip()
            if text_content:
                sections.append({
                    "class-name": class_name,
                    "type": "text",
                    "content": text_content
                })

    # Ghi vào file JSON
    output_data = {"sections": sections}

    with open("output-one-element.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print("Đã lưu dữ liệu vào output-one-element.json 🎯")




