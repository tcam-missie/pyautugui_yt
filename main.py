import pyautogui
import easyocr
import time
import random
import subprocess
import sys
import requests

old_url = "https://raw.githubusercontent.com/anisidina29/anisidina29-selenium_earnvids_docker/refs/heads/main/earnvids.txt"
response_old = requests.get(old_url)
response_old.raise_for_status()
links = response_old.text.strip().splitlines()

# Chọn 1 link ngẫu nhiên
url = random.choice(links)
print(f"Da chon link: {url}")
print("Dang mo Chrome...")
subprocess.Popen(["start", "chrome", "--new-window", url, "--window-size=1280,720"], shell=True)

# 2. Chờ trình duyệt mở và tab chính load
time.sleep(6)
import pygetwindow as gw

KEEP_KEYWORDS = ["youtube", "chatgpt", "record"]

def get_chrome_windows():
    return [w for w in gw.getWindowsWithTitle('Chrome') if w.visible and w.title.strip() != ""]

# Xử lý tab
tabs = get_chrome_windows()
for w in tabs:
        title = w.title.lower()
        if any(k in title for k in KEEP_KEYWORDS):
            print(f"Giu tab: {w.title}")
        else:
            print(f"Dong tab: {w.title}")
            w.activate()
            time.sleep(3)
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(0.5)
subprocess.Popen(["start", "chrome", "--new-window", url, "--window-size=1280,720"], shell=True)
time.sleep(3)
# Get email and password from command line arguments
account = sys.argv[1]
EMAIL, PASSWORD = account.split('|')

# Initialize EasyOCR with Vietnamese and English
reader = easyocr.Reader(['vi', 'en'], verbose=False)

# Find text position function
def find_text_position(text_list):
    screenshot = pyautogui.screenshot()
    screenshot_path = "screenads.png"
    screenshot.save(screenshot_path)
    results = reader.readtext(screenshot_path)

    for (bbox, text, prob) in results:
        for t in text_list:
            if t.lower() in text.lower():
                (top_left, _, bottom_right, _) = bbox
                x = int((top_left[0] + bottom_right[0]) / 2)
                y = int((top_left[1] + bottom_right[1]) / 2)
                return (x, y)
    return None

# Skip ad function
def skip_ad():
    try:
        skip_btn = find_text_position(["Skip", "Skip Ads"])
        if skip_btn:
            pyautogui.moveTo(*skip_btn, duration=0.3)
            #pyautogui.click()
            print("Clicked Skip Ad button")
    except Exception as e:
        print(f"[ERROR] Error while skipping ad: {e}")

# Launch Chrome in fullscreen (NOT incognito)
chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'
video_url = "https://www.youtube.com"
subprocess.Popen(["start", "chrome", "--new-window", video_url, "--window-size=1280,720"], shell=True)

# Wait for Chrome and YouTube to load
time.sleep(5)
tabs = get_chrome_windows()
for w in tabs:
        title = w.title.lower()
        if any(k in title for k in KEEP_KEYWORDS):
            print(f"Giu tab: {w.title}")
        else:
            print(f"Dong tab: {w.title}")
            w.activate()
            time.sleep(3)
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(0.5)

video_url = "https://www.youtube.com"
subprocess.Popen(["start", "chrome", "--new-window", video_url, "--window-size=1280,720"], shell=True)
time.sleep(5)
# Take screenshot for OCR
screenshot = pyautogui.screenshot()
screenshot_path = "screen.png"
screenshot.save(screenshot_path)

# Use OCR to detect "Sign in" button
results = reader.readtext(screenshot_path)
found = False
for (bbox, text, prob) in results:
    if "sign" in text.lower():
        print(f"Found: {text} (confidence {prob:.2f})")
        (top_left, top_right, bottom_right, bottom_left) = bbox
        x = int((top_left[0] + bottom_right[0]) / 2)
        y = int((top_left[1] + bottom_right[1]) / 2)
        pyautogui.moveTo(x, y, duration=0.5)
        for _ in range(3):  # Click 3 times
            pyautogui.click()
            time.sleep(0.2)
        found = True
        break

if not found:
    print("Sign in button not found!")

time.sleep(5)  # Wait for login page

# Enter email
pyautogui.typewrite(EMAIL)
time.sleep(3)
pyautogui.press('enter')
time.sleep(3)

# Enter password
pyautogui.typewrite(PASSWORD)
pyautogui.press('enter')
print("Login attempt finished (if email/password is correct)")
time.sleep(5)

# Function to get links from GitHub
def get_video_links():
    url = "https://raw.githubusercontent.com/anisidina29/pyautogui_yt/refs/heads/main/links.txt"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            links = [line.strip() for line in response.text.splitlines() if line.strip()]
            random.shuffle(links)
            print(f"[INFO] Retrieved {len(links)} links from GitHub")
            return links
        else:
            print("[WARNING] Failed to retrieve links")
            return []
    except Exception as e:
        print(f"[ERROR] Could not fetch links: {e}")
        return []

# Get initial links
video_links = get_video_links()
current_index = 0

# Function to open a video
opened_tabs = 0  # Biến toàn cục theo dõi số tab

def open_video(link):
    global opened_tabs
    subprocess.Popen(["start", "chrome", "--new-window", link, "--window-size=1280,720"], shell=True)
    opened_tabs += 1
    time.sleep(8)  # Đợi trang tải

    # Nếu có hơn 4 tab thì đóng tab cũ
    if opened_tabs > 4:
        pyautogui.hotkey('ctrl', 'w')
        opened_tabs -= 1
        print("[INFO] Closed old tab because more than 4 tabs were open.")

    # Di chuyển chuột ra giữa màn hình
    screen_width, screen_height = pyautogui.size()
    pyautogui.moveTo(screen_width // 2, screen_height // 2, duration=0.5)
    print(f"[INFO] Playing video: {link}")
    
# Human-like action simulation
import pyautogui
import random
import time

def human_like_action():
    actions = (
        ["move_mouse"] * 5 +  # 50%
        ["idle"] * 2 +        # 20%
        ["backward", "forward", "volume_up", "volume_down",
         "mute", "subtitle", "pause_play", "speed_up", "speed_down"] +  # 30%
        ["like"]              # ~5%
    )

    action = random.choice(actions)

    if action == "backward":
        pyautogui.press('j')
        print("[ACTION] Rewind 10s")
    elif action == "forward":
        pyautogui.press('l')
        print("[ACTION] Forward 10s")
    elif action == "volume_up":
        pyautogui.press('up')
        print("[ACTION] Volume up")
    elif action == "volume_down":
        pyautogui.press('down')
        print("[ACTION] Volume down")
    elif action == "mute":
        pyautogui.press('m')
        print("[ACTION] Mute/Unmute")
    elif action == "subtitle":
        pyautogui.press('c')
        print("[ACTION] Toggle subtitles")
    elif action == "pause_play":
        pyautogui.press('k')
        print("[ACTION] Play/Pause video")
    elif action == "speed_up":
        pyautogui.hotkey('shift', '>')
        print("[ACTION] Speed up")
    elif action == "speed_down":
        pyautogui.hotkey('shift', '<')
        print("[ACTION] Speed down")
    elif action == "move_mouse":
        x = random.randint(200, 1200)
        y = random.randint(200, 700)
        pyautogui.moveTo(x, y, duration=0.5)
        print(f"[ACTION] Mouse moved to ({x},{y})")
    elif action == "idle":
        print("[ACTION] Idle (do nothing)")
    elif action == "like":
        print("[ACTION] Trying to click Like button...")
        try:
            like_button = pyautogui.locateOnScreen('like_button.png', confidence=0.8)
            if like_button:
                center = pyautogui.center(like_button)
                pyautogui.click(center)
                print("[ACTION] Clicked Like button")
            else:
                print("[ACTION] Like button not found on screen")
        except Exception as e:
            print(f"[ERROR] Failed to click Like button: {e}")
            
# Start watching videos
print("Starting video watching automation...")

MAX_TABS = 4  # Giới hạn số tab

def close_extra_tabs():
    global opened_tabs
    while opened_tabs > MAX_TABS:
        pyautogui.hotkey('ctrl', 'w')
        opened_tabs -= 1
        time.sleep(0.5)
        print("[INFO] Closed extra tab.")

print("Starting video watching automation...")

while True:
    try:
        # Lấy lại danh sách video nếu đã hết link
        if current_index >= len(video_links):
            video_links = get_video_links()
            current_index = 0

        # Kiểm tra số tab trước khi mở video mới
        if opened_tabs >= MAX_TABS:
            print("[INFO] Max tabs reached, closing one tab before opening a new one.")
            pyautogui.hotkey('ctrl', 'w')
            opened_tabs -= 1
            time.sleep(1)

        # Mở video mới
        open_video(video_links[current_index])
        current_index += 1

        # Đảm bảo không có tab thừa
        close_extra_tabs()

        # Thời gian xem video
        watch_time = random.randint(300, 800)  # 5–13 phút
        start_time = time.time()
        print(f"[INFO] Watching video for {watch_time // 60} min...")

        screenshot_count = 0  # Biến đếm để đặt tên file ảnh
        
        # Xem video và thực hiện hành động mô phỏng
        while time.time() - start_time < watch_time:
            skip_ad()
            human_like_action()
            
            # Chụp ảnh màn hình
            screenshot = pyautogui.screenshot()
            screenshot_path = f"screenshot_{screenshot_count}.png"
            screenshot.save(screenshot_path)
            print(f"[DEBUG] Saved screenshot to {screenshot_path}")
            screenshot_count += 1
        
            time.sleep(random.randint(100, 200))  # Delay giữa các hành động

    except Exception as e:
        print(f"[ERROR] Main loop error: {e}")
