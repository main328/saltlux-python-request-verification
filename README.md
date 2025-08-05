# saltlux-python-request-verification
추출한 URL 주소에 대한 검증을 위한 정규화 프로그램.

## 기능
- 손쉬운 사용을 위한 직관적인 GUI 제공.
- 엑셀 파일 기반의 검증 수행 및 결과 제공.
- 서버 리다이렉션을 통해 요청 주소에 대한 정규화.
- 병렬 처리를 통해 다량의 요청 주소 검증 시간 단축.
- 프로그램 실행 시, 필요한 폴더 및 설정 파일 생성.

## 실행 방법
1. Python 3.8 이상이 설치되어 있어야 합니다.

2. 가상환경 생성 및 활성화:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

3. 필수 의존성 설치:
```bash
pip install -r requirements.txt
```

4. 환경 파일 생성:
```bash
cp .env_sample .env
```
`.env` 파일을 생성하고, 열어 환경 설정을 진행:
- `REQUEST_COLUMN`: 요청할 URL 주소 열 이름.
- `REQUEST_TIMEOUT`: 서버 요청 타임아웃.
- `MAX_THREADS`: 동시 처리 스레드 개수.
- `APP_ICON_NAME`: 실행 파일의 아이콘 이름.

## 사용 방법
### 프로그램 실행:
```bash
python main.py
```
- 실행에 필요한 기본적인 폴더 구조를 확인하여 자동 초기화.
- 사용자가 설정 파일을 생성하지 않아도 자동으로 설정 파일 생성.

### 실행 파일 기본 생성:
```bash
pyinstaller --onefile --windowed main.py
```
- `--onefile`: 실행에 필요한 모든 파일을 하나의 실행 파일로 압축.
- `--windowed`: 프로그램 실행 시 콘솔창을 제외하고 GUI 애플리케이션 출력.

### 실행 파일 고급 생성:
```bash
pyinstaller main.py `
    --onefile `
    --windowed `
    --name "요청 주소 검증 도구" `
    --icon="resources/assets/icon_v0.1.ico" `
    --add-data "resources;resources"
```
#### 명령어 옵션
- `--name`: 실행 파일의 이름을 지정.
- `--icon`: 실행 파일의 아이콘을 지정.
- `--add-data`: 외부 데이터를 실행 파일에 포함.