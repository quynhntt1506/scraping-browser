from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crawl_data import extract_texts
from news_extract import *
import time

# Đường dẫn đến ChromeDriver
CHROME_DRIVER_PATH = "chromedriver.exe"
WEBSITE_URL = "https://vietnamnet.vn/"

def setup_driver():
    """ Khởi tạo WebDriver """
    service = Service(CHROME_DRIVER_PATH)
    options = Options()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def load_website(driver, url):
    """ Mở trang web và full màn hình """
    driver.get(url)
    driver.maximize_window()

def inject_mouse_tracking_script(driver):
    """ Inject JavaScript để theo dõi vị trí chuột """
    driver.execute_script("""
        document.addEventListener('mousemove', function(event) {
            window.mouseX = event.clientX;
            window.mouseY = event.clientY;
        });
    """)
    print("🔹 Di chuyển chuột trong trình duyệt để kiểm tra vị trí.")

def get_mouse_position(driver):
    """ Lấy vị trí hiện tại của chuột từ JavaScript """
    x = driver.execute_script("return window.mouseX;")
    y = driver.execute_script("return window.mouseY;")
    return x, y

def get_element_at_position(driver, x, y):
    """ Lấy phần tử tại vị trí chuột """
    return driver.execute_script("return document.elementFromPoint(arguments[0], arguments[1]);", x, y)

def inject_highlight_script(driver):
    """ Inject JavaScript để highlight phần tử khi di chuột """
    driver.execute_script("""
        // Tạo style nếu chưa có
        if (!document.getElementById('highlight-style')) {
            let style = document.createElement('style');
            style.id = 'highlight-style';
            style.innerHTML = '.highlight-border { border: 2px solid red !important; }';
            document.head.appendChild(style);
        }

        // Hàm lấy selector
        function getSelector(tag, className) {
            let classSelector = className.trim().split(/\\s+/).join(".");
            return tag + (classSelector ? "." + classSelector : "");
        }

        let currentElements = new Set();
        let lastHoveredElements = new Set();

        function clearHighlights() {
            currentElements.forEach(el => el.classList.remove('highlight-border'));
            currentElements.clear();
        }
        function clearFormatClass(classString) {
            const regex = /^(mb|ml|mt|mr|p|pl|pr|pt|pb|text|bg)-\d+$/;
            return classString.split(" ").filter(cls => !regex.test(cls)).join(" ")
        }

        document.addEventListener('mousemove', function(event) {
            let el = document.elementFromPoint(event.clientX, event.clientY);
            if (!el || !el.parentElement) return;

            let tagName = el.tagName.toLowerCase();
            let className = el.className.trim();
            let parent = el.parentElement;

            let elements = [...parent.children].filter(child => 
                child.tagName.toLowerCase() === tagName && (clearFormatClass(child.className.trim()).includes(clearFormatClass(className)) || clearFormatClass(className).includes(clearFormatClass(child.className.trim())))    
            );

            let newHoveredElements = new Set(elements);
            let hasCommonElements = [...newHoveredElements].some(el => lastHoveredElements.has(el));

            if (!hasCommonElements) {
                clearHighlights();
            }

            elements.forEach(ele => {
                ele.classList.add('highlight-border');
                currentElements.add(ele);
            });

            lastHoveredElements = newHoveredElements;
        });

        document.addEventListener('mouseleave', clearHighlights);

        document.addEventListener('click', function() {
            let elements = [...document.querySelectorAll('.highlight-border')];
            let elementsData = elements.map(el => el.outerHTML);
            window.highlightedElements = elementsData;
        });
    """)

def get_highlighted_elements(driver):
    """ Lấy danh sách phần tử đã được highlight """
    return driver.execute_script("return window.highlightedElements || [];")

def save_highlighted_elements(elements, filename="highlighted_elements.html"):
    """ Ghi danh sách phần tử highlight vào file HTML """
    with open(filename, "w", encoding="utf-8") as file:
        # scraping data and write to json file
        scraping_data (elements)

        # write html to highlighted_elements.html
        file.write("<html><body>\n")
        file.write("<h2>Các phần tử được highlight:</h2>\n")
        for element in elements:
            file.write(f"{element}\n")
            print(extract_texts(element))
            # scraping_data_one_element(element)
            
        file.write("</body></html>")
    print(f"✅ Đã lưu các phần tử highlight vào `{filename}`")

def handle_choose_data(driver, url):
    """ Chương trình chính """
    load_website(driver, url)
    inject_mouse_tracking_script(driver)
    inject_highlight_script(driver)
    try:
        while True:
            x, y = get_mouse_position(driver)
            element = get_element_at_position(driver, x, y)
            if element:
                tag_name = element.tag_name
                class_name = element.get_attribute("class")
                if tag_name:
                    print(f"📍 Vị trí chuột: ({x}, {y}) - Tag: {tag_name}, Class: {class_name}")
                    input("👉 Nhấn Enter sau khi click vào phần tử cần lấy...")
                    print('URL NÈ: ',url, '\n-------\n', driver.current_url)
                    # nếu trang bị chuyển hướng
                    # ===========
                    if url != driver.current_url:
                        handle_choose_data(driver, driver.current_url)
                        return
                    # ===========
                    highlighted_elements = get_highlighted_elements(driver)
                    if highlighted_elements:
                        save_highlighted_elements(highlighted_elements)
                    else:
                        print("⚠ Không có phần tử nào được highlight.")

            time.sleep(0.5)  # Giảm tải CPU

    except KeyboardInterrupt:
        print("\n⏹ Dừng chương trình.")
        driver.quit()
    finally:
        driver.quit()

if __name__ == "__main__":    
    driver = setup_driver()
    handle_choose_data(driver, WEBSITE_URL)



