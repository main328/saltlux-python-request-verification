import os
from pathlib import Path
from dotenv import load_dotenv

from app import __version__

load_dotenv(Path(__file__).parent.parent / '.env', override=True)

class Config:
    # 기본 폴더 경로 정보.
    BASE_PATH: Path = Path(__file__).parent.parent
    RESOURCE_PATH: Path = BASE_PATH / 'resources'
    ASSETS_PATH: Path = RESOURCE_PATH / 'assets'

    # 애플리케이션 기본 정보.
    APP_TITLE: str = '요청 주소 검증 및 정규화 도구'
    APP_VERSION: str = f'v{__version__}'
    APP_ICON_NAME: str = os.getenv('APP_ICON_NAME', 'icon_v0.1.ico')

    # 인터페이스 기본 정보.
    WINDOW_WIDTH: int = 600
    WINDOW_HEIGHT: int = 450

    # 데이터 처리 정보.
    REQUEST_COLUMN: str = os.getenv('REQUEST_COLUMN', '요청 주소')
    REQUEST_TIMEOUT: int = int(os.getenv('REQUEST_TIMEOUT', 10))
    MAX_THREADS: int = int(os.getenv('MAX_THREADS', 10))

    # 필수 폴더 초기 생성.
    @classmethod
    def setup(cls) -> None:
        cls.RESOURCE_PATH.mkdir(parents=True, exist_ok=True)
        cls.ASSETS_PATH.mkdir(parents=True, exist_ok=True)