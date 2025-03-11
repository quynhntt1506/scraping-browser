from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Đường dẫn đến ChromeDriver
chrome_driver_path = "chromedriver.exe"

# Tạo Service
service = Service(chrome_driver_path)

# Tạo ChromeOptions (có thể bỏ qua nếu không cần tuỳ chỉnh)
options = Options()

# Khởi tạo WebDriver đúng cách

driver = webdriver.Chrome(service=service, options=options)

# Mở trang web
website = 'https://vnexpress.net/bo-tai-chinh-phai-trinh-nghi-quyet-ve-quan-ly-tien-ao-tuan-nay-4858810.html'
driver.get(website)

#mở full màn hình
driver.maximize_window()

#Set up a 30 seconds webdriver wait
# explicit_wait30 = WebDriverWait(browser, 30)
# driver.implicitly_wait(30)

driver.execute_script("""
    document.addEventListener('click', function(event) {
        window.mouseClickX = event.clientX;
        window.mouseClickY = event.clientY;
    });
""")

# Chờ người dùng click rồi lấy vị trí
input("Click vào trang web, sau đó nhấn Enter...")
click_x = driver.execute_script("return window.mouseClickX;")
click_y = driver.execute_script("return window.mouseClickY;")

print(f"Chuột đã click tại: ({click_x}, {click_y})")

# Lấy element tại vị trí click
element = driver.execute_script("return document.elementFromPoint(arguments[0], arguments[1]);", click_x, click_y)

# Hiển thị thông tin element nếu tồn tại
if element:
    tag_name_check = element.tag_name.lower()
    # kiểm tra xem vị trí đã click có phải thẻ a không
    if tag_name_check == 'a':
        # lấy link của thẻ a 
        link_url = element.get_attribute("href")
        if link_url:
            print(f"Đang chuyển hướng đến đường dẫn: {link_url}")
            driver.get(link_url) 
    # kiểm tra phần tử có URL không
    elif "href" in element.get_attribute("outerHTML"):
        link_url = element.get_attribute("href")
        if link_url:
            print(f"Đang chuyển hướng đến đường dẫn: {link_url}")
            driver.get(link_url) 
    else:
        tag_name = element.tag_name
        class_name = element.get_attribute('class')
        print(f"Element tại vị trí click ({click_x}, {click_y}):")
        print(f"- Tag: {element.tag_name}")
        print(f"- ID: {element.get_attribute('id')}")
        print(f"- Class: {element.get_attribute('class')}")
        print(f"- Text: {element.text}")
        print(f"- HTML: {element.get_attribute('outerHTML')}")

        selector = f"{tag_name}.{class_name.replace(' ', '.')}" if class_name else tag_name
        driver.execute_script(f"""
            let elements = document.querySelectorAll('{selector}');
            elements.forEach(el => el.style.border = '2px solid red');
        """)
        matching_elements = driver.find_elements("css selector", f"{element.tag_name}.{element.get_attribute('class').replace(' ', '.')}")
        print("\nCác phần tử có cùng tag và class:")
        for idx, el in enumerate(matching_elements, 1):
            print(f"{idx}. {el.get_attribute('outerHTML')[:100]}...")  # Hiển thị một phần mã HTML
    
else:
    print("Không tìm thấy element tại vị trí click!")


## =================================================
## get element from mouse position 
# # Move the mouse to a specific position (x, y)
# x, y = 500, 300  # Example coordinates
# actions = ActionChains(driver)
# actions.move_by_offset(x, y).perform()

# # Use JavaScript to get the element at the mouse position
# element = driver.execute_script("return document.elementFromPoint(arguments[0], arguments[1]);", x, y)

# # Print the element details
# if element:
#     print("Tag:", element.tag_name)
#     print("Text:", element.text)
#     print("Attributes:", element.get_attribute("outerHTML"))
# else:
#     print("No element found at the position.")
## ===================================================
# Keep the browser open
input("Press Enter to close the browser...")
driver.quit()



# try:
#     while True:
#         pass  # Keeps the script running indefinitely
# except KeyboardInterrupt:
#     driver.quit()  # Ensure WebDriver quits when interrupted


# Đóng trình duyệt
# driver.quit()