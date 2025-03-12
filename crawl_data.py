from bs4 import BeautifulSoup
#KHÔNG DÙNG
## get text
# def extract_texts(html):
#     soup = BeautifulSoup(html, "html.parser")
#     data = {}

#     for element in soup.find_all():
#         tag_name = element.name
#         # lấy nội dung và loại bỏ khoảng trắng thừa
#         text = element.get_text(strip=True)
#         if text and not any(child.name for child in element.find_all()):
#             if tag_name not in data:
#                 data[tag_name] = set()
#             data[tag_name].add(text)
#     return data


#nếu elements có một phần tử, lấy thông tin từ các thẻ con và xuống dòng (mỗi phần một dòng) - có thể hỗ trợ người dùng thêm title (nếu cần)


#nếu elements có nhiều phần tử, vói mỗi thẻ con có tag giống nhau và cùng cấp, lấy thông tin ra và đưa vào cùng bảng
 

def extract_texts(html):
    soup = BeautifulSoup(html, "html.parser")
    extracted_data = []

    def traverse(element):
        # Kiểm tra nếu là tag (không phải NavigableString)
        if element.name:
            text = element.get_text(strip=True)  # Lấy nội dung văn bản
            class_name = " ".join(element.get("class", []))  # Lấy class nếu có
            if text:
                extracted_data.append((text, class_name))
            
            # Duyệt tiếp các phần tử con
            for child in element.children:
                if hasattr(child, "children"):  # Chỉ duyệt tiếp nếu là tag
                    traverse(child)

    traverse(soup.body or soup)
    return extracted_data

# Đọc dữ liệu HTML từ file hoặc biến
# html = """<div class="box highlight-border">
#       <div class="box-head">
#         <h3>
#           <a
#             href="/kinh-doanh/net-zero"
#             data-itm-source="#vn_source=Home&amp;vn_campaign=Box-NetZero&amp;vn_medium=Title&amp;vn_term=Desktop"
#             title="netzero"
#             data-itm-added="1"
#             ><img
#               src="https://s1.vnecdn.net/vnexpress/restruct/i/v9559/graphics/netzero.png"
#               alt="netzero"
#           /></a>
#         </h3>
#         <h3>
#           <a
#             href="/kinh-doanh/net-zero/cam-nang-net-zero"
#             data-itm-source="#vn_source=Home&amp;vn_campaign=Box-NetZero&amp;vn_medium=CamNang&amp;vn_term=Desktop"
#             title="Cẩm nang"
#             data-itm-added="1"
#             >Cẩm nang</a
#           >
#         </h3>
#         <h3 class="hidden-mb">
#           <a
#             href="/kinh-doanh/net-zero/hanh-tinh-keu-cuu"
#             data-itm-source="#vn_source=Home&amp;vn_campaign=Box-NetZero&amp;vn_medium=HanhTinhKeuCuu&amp;vn_term=Desktop"
#             title="Hành tinh kêu cứu"
#             data-itm-added="1"
#             >Hành tinh kêu cứu</a
#           >
#         </h3>
#         <h3 class="hidden-mb">
#           <a
#             href="/kinh-doanh/net-zero/chinh-sach"
#             data-itm-source="#vn_source=Home&amp;vn_campaign=Box-NetZero&amp;vn_medium=ChinhSach&amp;vn_term=Desktop"
#             title="Chính sách"
#             data-itm-added="1"
#             class=""
#             >Chính sách</a
#           >
#         </h3>
#         <h3>
#           <a
#             href="/kinh-doanh/net-zero/doanh-nghiep-xanh"
#             data-itm-source="#vn_source=Home&amp;vn_campaign=Box-NetZero&amp;vn_medium=DoanhNghiepXanh&amp;vn_term=Desktop"
#             title="Doanh nghiệp xanh"
#             data-itm-added="1"
#             class=""
#             >Doanh nghiệp xanh</a
#           >
#         </h3>
#       </div>
#       <article class="item-news">
#         <div class="thumb-art">
#           <a
#             href="https://vnexpress.net/chat-thai-tu-khai-thac-mo-thanh-co-hoi-ty-usd-trong-kinh-te-net-zero-4859041.html"
#             class="thumb thumb-5x3"
#             data-itm-source="#vn_source=Home&amp;vn_campaign=Box-NetZero&amp;vn_medium=Item-1&amp;vn_term=Desktop"
#             title="Chất thải từ khai thác mỏ thành cơ hội tỷ USD trong kinh tế Net Zero"
#             data-itm-added="1"
#           >
#             <picture>
#               <!--[if IE 9]><video style="display: none;"><![endif]-->
#               <source
#                 data-srcset="https://i1-kinhdoanh.vnecdn.net/2025/03/10/mining-large-1741580583-174158-7838-8013-1741581295.png?w=120&amp;h=72&amp;q=100&amp;dpr=1&amp;fit=crop&amp;s=nutzi_7xw2BxzMmiZ1Bvbw 1x, https://i1-kinhdoanh.vnecdn.net/2025/03/10/mining-large-1741580583-174158-7838-8013-1741581295.png?w=120&amp;h=72&amp;q=100&amp;dpr=2&amp;fit=crop&amp;s=FEpG394Y7Ahalynw66o0Tg 2x"
#                 srcset="
#                   https://i1-kinhdoanh.vnecdn.net/2025/03/10/mining-large-1741580583-174158-7838-8013-1741581295.png?w=120&amp;h=72&amp;q=100&amp;dpr=1&amp;fit=crop&amp;s=nutzi_7xw2BxzMmiZ1Bvbw 1x,
#                   https://i1-kinhdoanh.vnecdn.net/2025/03/10/mining-large-1741580583-174158-7838-8013-1741581295.png?w=120&amp;h=72&amp;q=100&amp;dpr=2&amp;fit=crop&amp;s=FEpG394Y7Ahalynw66o0Tg 2x
#                 "
#               />
#               <!--[if IE 9]></video><![endif]-->
#               <img
#                 loading="lazy"
#                 intrinsicsize="120x72"
#                 alt="Chất thải từ khai thác mỏ thành cơ hội tỷ USD trong kinh tế Net Zero"
#                 class="lazy lazied"
#                 src="https://i1-kinhdoanh.vnecdn.net/2025/03/10/mining-large-1741580583-174158-7838-8013-1741581295.png?w=120&amp;h=72&amp;q=100&amp;dpr=1&amp;fit=crop&amp;s=nutzi_7xw2BxzMmiZ1Bvbw"
#                 data-src="https://i1-kinhdoanh.vnecdn.net/2025/03/10/mining-large-1741580583-174158-7838-8013-1741581295.png?w=120&amp;h=72&amp;q=100&amp;dpr=1&amp;fit=crop&amp;s=nutzi_7xw2BxzMmiZ1Bvbw"
#                 data-ll-status="loaded"
#               />
#             </picture>
#           </a>
#         </div>
#         <div class="content-art">
#           <h3 class="title-news">
#             <a
#               href="https://vnexpress.net/chat-thai-tu-khai-thac-mo-thanh-co-hoi-ty-usd-trong-kinh-te-net-zero-4859041.html"
#               data-itm-source="#vn_source=Home&amp;vn_campaign=Box-NetZero&amp;vn_medium=Item-1&amp;vn_term=Desktop"
#               title="Chất thải từ khai thác mỏ thành cơ hội tỷ USD trong kinh tế Net Zero"
#               data-itm-added="1"
#               >Chất thải từ khai thác mỏ thành cơ hội tỷ USD trong kinh tế Net
#               Zero</a
#             >
#             <span class="meta-news">
#               <a
#                 class="count_cmt"
#                 href="https://vnexpress.net/chat-thai-tu-khai-thac-mo-thanh-co-hoi-ty-usd-trong-kinh-te-net-zero-4859041.html#box_comment_vne"
#                 style="white-space: nowrap; display: none"
#               >
#                 <svg class="ic ic-comment">
#                   <use xlink:href="#Comment-Reg"></use>
#                 </svg>
#                 <span class="font_icon widget-comment-4859041-1"></span>
#               </a>
#             </span>
#           </h3>
#           <p class="short_intro">
#             <a
#               href="https://vnexpress.net/chat-thai-tu-khai-thac-mo-thanh-co-hoi-ty-usd-trong-kinh-te-net-zero-4859041.html"
#               data-itm-source="#vn_source=Home&amp;vn_campaign=Box-NetZero&amp;vn_medium=Item-1&amp;vn_term=Desktop"
#               title="Chất thải từ khai thác mỏ thành cơ hội tỷ USD trong kinh tế Net Zero"
#               data-itm-added="1"
#               >31 tỷ tấn chất thải mỏ có thể chuyển hóa thành "bể chứa carbon"
#               chất lượng cao, mang về hàng trăm tỷ USD từ việc bán tín chỉ.</a
#             >
#           </p>
#         </div>
#       </article>
#       <div class="timline">
#         <h3 class="title">
#           <a
#             href="https://vnexpress.net/sieu-thi-gap-kho-khi-tim-cach-thay-khay-nhua-bao-quan-thuc-pham-4857288.html"
#             data-itm-source="#vn_source=Home&amp;vn_campaign=Box-NetZero&amp;vn_medium=Item-2&amp;vn_term=Desktop"
#             title="Siêu thị gặp khó khi tìm cách thay khay nhựa bảo quản thực phẩm"
#             data-itm-added="1"
#             >Siêu thị gặp khó khi tìm cách thay khay nhựa bảo quản thực phẩm</a
#           >
#           <span class="meta-news">
#             <a
#               class="count_cmt"
#               href="https://vnexpress.net/sieu-thi-gap-kho-khi-tim-cach-thay-khay-nhua-bao-quan-thuc-pham-4857288.html#box_comment_vne"
#               style="white-space: nowrap; display: inline-block"
#             >
#               <svg class="ic ic-comment">
#                 <use xlink:href="#Comment-Reg"></use>
#               </svg>
#               <span class="font_icon widget-comment-4857288-1">41</span>
#             </a>
#           </span>
#         </h3>
#       </div>
#     </div>"""  # Thay bằng nội dung HTML của bạn
# data = extract_text_with_class(html)

# # In kết quả
# for text, class_name in data:
#     print(f"Class: {class_name} | Text: {text}")
