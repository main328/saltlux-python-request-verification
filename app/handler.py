import pandas
from pathlib import Path
from typing import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.config import Config
from app.validator import Validator

class Handler:
    def process_requests_from_file(
        self,
        xlsx_path: Path,
        column: str,
        callback: Callable[[int, int], None]
    ) -> pandas.DataFrame:
        '''
        Args:
            xlsx_path (str): 검증을 진행할 요청 주소가 담긴 xlsx 파일 경로.
            column (str): 검증을 진행할 요청 주소 열 이름.
            callback (Callable[[int, int], None]): 현재 진행 수, 전체 수를 인자로 받는 진행 상황 콜백 함수.
        Returns:
            pandas.DataFrame: 검증 결과(요청 주소, 응답 주소, 응답 상태, 오류 내용)가 담긴 데이터프레임.
        '''
        try:
            dataframe = pandas.read_excel(xlsx_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"입력 파일을 찾을 수 없습니다: {xlsx_path}")

        if column not in dataframe.columns:
            raise KeyError(f'요청 주소 열을 찾을 수 없습니다: {column}')

        requests_to_check = dataframe[column].dropna().tolist()
        total_requests = len(requests_to_check)
        
        validate_results = []
        
        with ThreadPoolExecutor(max_workers=Config.MAX_THREADS) as executor:
            future_to_request = {executor.submit(Validator.get_final_response, request): request for request in requests_to_check}
            
            for index, future in enumerate(as_completed(future_to_request)):
                try:
                    result = future.result()
                    validate_results.append(result)
                except Exception as exc:
                    original_request = future_to_request[future]
                    validate_results.append((original_request, "", "Execution Error", str(exc)))
                
                # UI 업데이트를 위해 콜백 함수 호출
                if callback:
                    callback(index + 1, total_requests)

        return pandas.DataFrame(validate_results, columns=['Original_request', 'Final_request', 'Status_Code', 'Error_Message'])

    def save_results_to_excel(
            self,
            dataframe: pandas.DataFrame,
            output_path: Path
        ) -> None:
        '''
        Args:
            dataframe (pandas.DataFrame): xlsx 파일로 저장할 데이터프레임.
            output_path (Path): 검증 결과를 저장할 xlsx 파일 경로.
        Returns:
            None
        '''
        dataframe.to_excel(output_path, index=False)
