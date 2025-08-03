import pyautogui
import easyocr
import time
import random
import subprocess
import sys

# Get email and password from command line arguments
EMAIL = sys.argv[1]
PASSWORD = sys.argv[2]

# Initialize EasyOCR with Vietnamese and English
reader = easyocr.Reader(['vi', 'en'])

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
            pyautogui.click()
            print("Clicked Skip Ad button")
    except Exception as e:
        print(f"[ERROR] Error while skipping ad: {e}")

# Launch Chrome in incognito mode
chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'
video_url = "https://www.youtube.com"
subprocess.Popen(f'{chrome_path} --incognito {video_url}')

# Wait for Chrome and YouTube to load
time.sleep(5)

# Take screenshot for OCR
screenshot = pyautogui.screenshot()
screenshot_path = "screen.png"
screenshot.save(screenshot_path)

# Use OCR to detect "Sign in" button
results = reader.readtext(screenshot_path)
found = False
for (bbox, text, prob) in results:
    if "đăng nhập" in text.lower() or "sign in" in text.lower():
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

# Open video
video_url = "https://youtu.be/RtYwsTYhtJo?si=2DF-CyvmqMHP8N2R"
subprocess.Popen(f'{chrome_path} --incognito {video_url}')
time.sleep(8)

# Get screen size
screen_width, screen_height = pyautogui.size()
video_x = screen_width // 2
video_y = screen_height // 2

# Click Play button
pyautogui.moveTo(video_x, video_y, duration=0.5)
pyautogui.click()
print("Clicked Play button")

# Find and click VTV function
def find_and_click_vtv():
    try:
        screenshot = pyautogui.screenshot()
        results = reader.readtext(screenshot)
        for (bbox, text, prob) in results:
            if "vtv" in text.lower():
                print(f"[INFO] Found '{text}' (confidence {prob:.2f})")
                (x_min, y_min), (x_max, y_max) = bbox[0], bbox[2]
                center_x = (x_min + x_max) // 2
                center_y = (y_min + y_max) // 2
                pyautogui.click(center_x, center_y - 100)
                print(f"[ACTION] Clicked 100px above at ({center_x}, {center_y - 100})")
                return True
        return False
    except Exception as e:
        print(f"[ERROR] OCR error: {e}")
        return False

# Human-like action simulation
def human_like_action():
    action = random.choice(["move_mouse", "scroll", "keyboard"])
    if action == "move_mouse":
        x = random.randint(500, 1000)
        y = random.randint(200, 600)
        pyautogui.moveTo(x, y, duration=0.5)
        print("[ACTION] Mouse moved")
    elif action == "scroll":
        pyautogui.scroll(random.choice([200, -200]))
        print("[ACTION] Page scrolled")
    elif action == "keyboard":
        key_action = random.choice(["left", "right"])
        pyautogui.press(key_action)
        print(f"[ACTION] Pressed {key_action}")

# Main loop
print("Starting video watching automation...")

while True:
    try:
        watch_time = random.randint(180, 300)  # 3–5 min
        start_time = time.time()
        print(f"[INFO] Watching video for {watch_time // 60} min...")

        while time.time() - start_time < watch_time:
            skip_ad()
            human_like_action()
            time.sleep(random.randint(20, 30))  # Perform action every 20–30s

        print("[INFO] Time's up, searching for new video...")
        if not find_and_click_vtv():
            print("[WARNING] VTV not found, scrolling...")
            pyautogui.scroll(-500)
            time.sleep(2)

    except Exception as e:
        print(f"[ERROR] Main loop error: {e}")
