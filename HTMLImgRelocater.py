import os
import re
import shutil
import urllib.parse
import sys

# 실행 파일의 절대 경로를 찾습니다.
exe_path = os.path.abspath(sys.argv[0])

# 실행 파일이 있는 폴더로 이동합니다.
exe_folder = os.path.dirname(exe_path)
os.chdir(exe_folder)
# 현재 폴더의 파일 목록을 출력합니다.
print("현재 폴더의 파일 목록:")
for item in os.listdir():
    print(f" - {item}")

#다운로드한 html파일의 이름 ex) index.html
HTML_FILE_NAME = input("다운로드한 html파일의 이름을 입력해주세요 (예: index.html): ")

# HTML 파일이 존재하는지 확인합니다.
if not os.path.exists(HTML_FILE_NAME):
    print(f"파일 {HTML_FILE_NAME} 이(가) 존재하지 않습니다. 파일 이름을 확인하고 다시 시도하세요.")
    exit()

#다운로드한 이미지 폴더의 이름 ex) images
IMAGES_FOLDER_NAME = input("다운로드한 이미지 폴더의 이름을 입력해주세요 (예: images): ")

# 이미지 폴더가 존재하는지 확인합니다.
if not os.path.exists(IMAGES_FOLDER_NAME):
    print(f"폴더 {IMAGES_FOLDER_NAME} 이(가) 존재하지 않습니다. 폴더 이름을 확인하고 다시 시도하세요.")
    exit()

RELOCATED_FOLDER_NAME = "Relocated_images"

# HTML 파일을 읽습니다.
with open(f'./{HTML_FILE_NAME}', 'r') as f:
    html = f.read()

matches = []
for match in re.findall(r'src="(.+?)"', html):
    if match.endswith('.png'):
        file_name = os.path.basename(match)
        decoded_name = urllib.parse.unquote(file_name)
        matches.append(decoded_name)

print("찾은 이미지:")
print(matches)

# 새로운 폴더를 만들어 이미지를 저장합니다.
if not os.path.exists(RELOCATED_FOLDER_NAME):
    os.makedirs(RELOCATED_FOLDER_NAME)
    print(f"'{RELOCATED_FOLDER_NAME}' 폴더를 생성했습니다.")
else:
    shutil.rmtree(RELOCATED_FOLDER_NAME)
    os.makedirs(RELOCATED_FOLDER_NAME)
    print(f"'{RELOCATED_FOLDER_NAME}' 폴더를 재생성했습니다.")

print("\n이미지 이동:")

used_names = set()
for i, match in enumerate(matches):
    old_name = match
    new_name = f'{i+1}.png'

    # 중복된 이미지가 발견될 경우, 넘버링을 바꾸어 파일 이름을 만듭니다.
    while new_name in used_names:
        i += 1
        new_name = f'{i+1}.png'

    used_names.add(new_name)
    print(f"{old_name} -> {new_name}")
    shutil.copy(os.path.join(IMAGES_FOLDER_NAME, old_name), os.path.join(RELOCATED_FOLDER_NAME, new_name))

print(f"\n모든 이미지가 {RELOCATED_FOLDER_NAME}로 복사되어 이동되었습니다!")
