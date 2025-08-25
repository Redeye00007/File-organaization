import os
import shutil

# ---------------- COLORS ---------------- #
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
RED = "\033[1;31m"
RESET = "\033[0m"

# ---------------- AUTO RENAME FUNCTION ---------------- #
def get_unique_path(dest_folder, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(dest_folder, new_filename)):
        new_filename = f"{base}({counter}){ext}"
        counter += 1

    return os.path.join(dest_folder, new_filename)

# ---------------- FILE ORGANIZER ---------------- #
def organize_files(folders, output_folder, recursive=True):
    if not folders:
        print(f"{RED}❌ No folders provided!{RESET}")
        return

    # Categories
    categories = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov"],
        "Music": [".mp3", ".wav", ".aac"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
        "Archives": [".zip", ".rar", ".tar", ".gz"],
        "Others": []
    }

    os.makedirs(output_folder, exist_ok=True)

    for folder_path in folders:
        if not os.path.exists(folder_path):
            print(f"{RED}❌ Folder not found: {folder_path}{RESET}")
            continue

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                moved = False

                for category, extensions in categories.items():
                    if ext in extensions:
                        dest_folder = os.path.join(output_folder, category)
                        os.makedirs(dest_folder, exist_ok=True)

                        unique_path = get_unique_path(dest_folder, file)

                        try:
                            shutil.move(file_path, unique_path)
                            print(f"{GREEN}📂 Moved {file} → {category}{RESET}")
                        except Exception as e:
                            print(f"{RED}⚠️ Error moving {file}: {e}{RESET}")
                        moved = True
                        break

                if not moved:
                    dest_folder = os.path.join(output_folder, "Others")
                    os.makedirs(dest_folder, exist_ok=True)

                    unique_path = get_unique_path(dest_folder, file)

                    try:
                        shutil.move(file_path, unique_path)
                        print(f"{YELLOW}📦 Moved {file} → Others{RESET}")
                    except Exception as e:
                        print(f"{RED}⚠️ Error moving {file}: {e}{RESET}")

            if not recursive:
                break

    print(f"\n{CYAN}✅ File organizing complete!{RESET}")

# ---------------- MAIN MENU ---------------- #
def main():
    while True:
        print(f"\n{CYAN}===== 🚀 PROJECT MENU ====={RESET}")
        print("1. Organize Files")
        print("2. Exit")

        choice = input("\n👉 Enter choice (1-2): ").strip()

        if choice == "1":
            while True:
                print(f"\n{CYAN}--- Organize Options ---{RESET}")
                print("1. Multiple Folder Selection")
                print("2. Default: Download Folder")
                print("3. Back to Main Menu")

                sub_choice = input("\n👉 Enter choice (1-3): ").strip()

                if sub_choice == "1":
                    folders = input("📂 Enter multiple folder paths (comma separated): ").split(",")
                    folders = [f.strip() for f in folders if f.strip()]
                    output_folder = os.path.join(os.path.expanduser("~"), "Organized")
                    organize_files(folders, output_folder)

                elif sub_choice == "2":
                    download_folder = os.path.join(os.path.expanduser("~"), "Download")
                    output_folder = os.path.join(os.path.expanduser("~"), "Organized")
                    organize_files([download_folder], output_folder)

                elif sub_choice == "3":
                    break
                else:
                    print(f"{RED}❌ Invalid choice!{RESET}")

        elif choice == "2":
            print(f"{CYAN}👋 Exiting... Bye!{RESET}")
            break
        else:
            print(f"{RED}❌ Invalid choice!{RESET}")

if __name__ == "__main__":
    main()
