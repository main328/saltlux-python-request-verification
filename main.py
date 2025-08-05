import os, sys, shutil
from pathlib import Path

from app.config import Config
from app.interface import Application

def setup_env() -> None:
    # Config의 setup() 함수를 통해 기본 폴더 구조 초기화.
    Config.setup()

    # 사용자가 .env 파일을 생성하지 않을 경우, 
    env_path = Config.BASE_PATH / '.env'
    env_sample_path = Config.BASE_PATH / '.env_sample'

    # .env 파일이 존재하지 않고, .env_sample 파일이 존재할 경우에만 복사
    if not env_path.exists() and env_sample_path.exists():
        print(f'INFO: {env_path} 파일이 존재하지 않아 {env_sample_path} 파일로 생성합니다.')
        try:
            shutil.copy(env_sample_path, env_path)
            print(f'INFO: {env_sample_path} 구성으로 {env_path}를 생성했습니다.')
        except Exception as error:
            print(f'ERROR: {env_sample_path} 파일 복사에 실패했습니다: {error}')

if __name__ == '__main__':
    # 환경 설정.
    setup_env()

    # GUI 생성을 위해 Application 클래스의 인스턴스 생성.
    app = Application()

    # 4. 아이콘 경로 설정.
    icon_path: Path = Config.ASSETS_PATH / Config.APP_ICON_NAME
    
    # ico 파일이 존재할 경우,
    if os.path.exists(icon_path):
        app.iconbitmap(icon_path)
    # ico 파일이 존재하지 않을 경우,
    else:
        print(f'WARNING: 아이콘 파일을 찾을 수 없습니다: {icon_path}')
        
    # 6. tkinter GUI 애플리케이션의 메인 루프를 시작합니다.
    app.mainloop()
