import os, re, random, requests, subprocess

KEY_FILE = ".fbtool_key"
GITHUB_KEY_URL = "https://github.com/TOOLSv1/FB_TOOL/blob/main/key.txt"
TOOL_REPO = "https://github.com/TOOLSv1/FB_TOOL.git"
TOOL_DIR = "FB_TOOL"
TOOL_FILE = "fb_tool.py"

def generate_key():
    rand_part = ''.join(random.choices("0123456789", k=8))
    return f"FB_TOOL-APPROVAL-KEY-{rand_part}"

def save_key_locally(key):
    with open(KEY_FILE, "w") as f:
        f.write(key)

def load_local_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE) as f:
            return f.read().strip()
    return None

def check_approval(key):
    try:
        r = requests.get(GITHUB_KEY_URL)
        return key in r.text
    except Exception as e:
        print(f"Error checking approval: {e}")
        return False

def run_fb_tool():
    try:
        if not os.path.exists(TOOL_DIR):
            print("Cloning tool repository...")
            subprocess.run(["git", "clone", TOOL_REPO], check=True)
        print("Running fb_tool.py...")
        os.system(f"python {os.path.join(TOOL_DIR, TOOL_FILE)}")
    except Exception as e:
        print(f"Error running fb_tool.py: {e}")

def main():
    key = load_local_key()
    if not key:
        key = generate_key()
        save_key_locally(key)
        print(f"\nYour generated approval key is:\n\n{key}\n\nSend this to admin for approval.\n")
        return

    print(f"Your saved key: {key}")
    if check_approval(key):
        print("Key approved! Launching fb_tool.py...")
        run_fb_tool()
    else:
        print("Your key is not approved yet. Please wait for admin approval.")

if __name__ == "__main__":
    main()
