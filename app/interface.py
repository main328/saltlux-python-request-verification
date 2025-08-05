import os, threading, tkinter
from pathlib import Path
from datetime import datetime
from tkinter import ttk, filedialog, messagebox

from app.config import Config
from app.handler import Handler

class Application(tkinter.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f'{Config.APP_TITLE} {Config.APP_VERSION}')
        self.geometry(f'{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}')
        
        # 데이터 처리를 담당할 핸들러 인스턴스 생성.
        self.handler = Handler()
        # 정의된 GUI 생성.
        self.create_widgets()

    def create_widgets(self) -> None:
        '''
        GUI를 구성하는 모든 위젯(버튼, 입력창, 라벨 등)을 생성하고 배치합니다.
        '''
        main_frame = ttk.Frame(self, padding='10')
        main_frame.pack(fill=tkinter.BOTH, expand=True)

        # 1. xlsx 파일 선택 영역.
        file_frame = ttk.LabelFrame(main_frame, text='1. 엑셀 파일 선택', padding='10')
        file_frame.pack(fill=tkinter.X, pady=5)

        self.xlsx_path_var = tkinter.StringVar()
        self.xlsx_path_entry = ttk.Entry(file_frame, textvariable=self.xlsx_path_var, state='readonly', width=50)
        self.xlsx_path_entry.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True, padx=(0, 5))
        self.browse_button = ttk.Button(file_frame, text='찾아보기', command=self.browse_file)
        self.browse_button.pack(side=tkinter.LEFT)

        # 2. 요청 주소의 열 이름 입력 영역.
        column_frame = ttk.LabelFrame(main_frame, text='2. 요청 주소의 열 이름 입력', padding='10')
        column_frame.pack(fill=tkinter.X, pady=5)
        
        self.column_name_var = tkinter.StringVar()
        self.column_name_entry = ttk.Entry(column_frame, textvariable=self.column_name_var, width=60)
        self.column_name_entry.pack(fill=tkinter.X)
        self.column_name_entry.insert(0, Config.REQUEST_COLUMN)

        # 3. 검증 수행 영역.
        # 3-1. 검증 수행 버튼 배치.
        self.start_button = ttk.Button(main_frame, text='검증 수행', command=self.start_processing)
        self.start_button.pack(pady=10, fill=tkinter.X)
        # 3-2. 검증 진행 현황 배치.
        progress_frame = ttk.LabelFrame(main_frame, text='진행 상황', padding='10')
        progress_frame.pack(fill=tkinter.BOTH, expand=True, pady=5)

        self.progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', mode='determinate')
        self.progress_bar.pack(fill=tkinter.X, pady=5)

        self.status_label_var = tkinter.StringVar()
        self.status_label_var.set('대기 중...')
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_label_var)
        self.status_label.pack(fill=tkinter.X, pady=5)

    # 찾아보기 선택 시, xlsx 파일 지정하기 위한 파일 탐색기 호출 함수.
    def browse_file(self) -> None:
        xlsx_path = filedialog.askopenfilename(
            title='검증을 수행할 파일을 선택하시기 바랍니다.',
            filetypes=(('Excel files', '*.xlsx *.xls'), ('All files', '*.*'))
        )
        if xlsx_path:
            self.xlsx_path_var.set(xlsx_path)

    # 검증 수행 선택 시, 요청 주소에 대한 검증 수행 함수.
    def start_processing(self) -> None:
        xlsx_path = self.xlsx_path_var.get()
        column_name = self.column_name_var.get()

        if not xlsx_path:
            messagebox.showerror('ERROR', 'xlsx 파일을 선택하시기 바랍니다.')
            return
        if not column_name:
            messagebox.showerror('ERROR', '요청 주소가 기입된 열 이름을 지정해주시기 바랍니다.')
            return
        
        thread = threading.Thread(target=self.process_requests_thread, args=(xlsx_path, column_name))
        thread.start()

    # 검증 수행 시, 진행 상황을 전달 받아 GUI의 진행률 바와 텍스트를 갱신하는 함수.
    def update_progress(self, current_step: int, total_steps: int) -> None:
        if self.progress_bar['maximum'] != total_steps:
            self.progress_bar['maximum'] = total_steps
        self.progress_bar['value'] = current_step
        self.status_label_var.set(f'처리 중... ({current_step}/{total_steps})')
        self.update_idletasks()

    # 검증 수행 시, Handler를 통해 처리된 데이터를 전달, 가공, 저장하는 함수.
    def process_requests_thread(self, xlsx_path: Path, column_name: str) -> None:
        self.start_button.config(state='disabled')
        self.status_label_var.set('파일을 읽는 중...')
        self.progress_bar['value'] = 0

        try:
            # Handler를 통해 처리된 데이터를 callback 함수로 전달.
            result_df = self.handler.process_requests_from_file(
                xlsx_path, column_name, self.update_progress
            )
            
            self.status_label_var.set('검증 결과를 저장할 파일 위치를 선택하시기 바랍니다.')

            timestamp = datetime.now().strftime('%Y%M%d%H%M%S')
            xlsx_name = os.path.splitext(os.path.basename(xlsx_path))[0]
            save_name = f'{timestamp}_{xlsx_name}_검증결과.xlsx'
            
            save_path: Path = filedialog.asksaveasfilename(
                title='요청 주소에 대한 검증 결과',
                initialfile=save_name,
                defaultextension='.xlsx',
                filetypes=(('Excel files', '*.xlsx'),)
            )

            if save_path:
                # Handler를 통해 검증 결과를 xlsx 파일로 저장.
                self.handler.save_results_to_excel(result_df, save_path)
                messagebox.showinfo('INFO', f'요청 주소에 대한 검증이 완료되어 결과가 파일로 저장되었습니다.\n파일 경로: {save_path}')
            else:
                messagebox.showwarning('WARNING', '저장이 취소되었습니다.')

        except (FileNotFoundError, KeyError) as e:
            # FileHandler에서 발생할 수 있는 특정 오류를 처리.
            messagebox.showerror('ERROR', str(e))
        except Exception as e:
            # 그 외 모든 예외에 대해 오류로 처리.
            messagebox.showerror('ERROR', f'처리 중 오류가 발생했습니다:\n{e}')
        finally:
            self.reset_ui()

    def reset_ui(self) -> None:
        self.start_button.config(state='normal')
        self.status_label_var.set('대기 중...')
        self.progress_bar['value'] = 0
