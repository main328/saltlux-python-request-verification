import requests

from app.config import Config

class Validator:
    @staticmethod
    def get_final_response(request: str) -> tuple:
        '''
        Args:
            request (str): 검증하고자하는 요청 주소 문자열.
        Returns:
            tuple: 검증 정보(요청 주소, 응답 주소, 응답 상태, 오류 내용)를 담은 튜플.
        '''
        # 요청 주소의 프로토콜이 존재하지 않을 경우,
        if not str(request).startswith(('http://', 'https://')):
            verification_request = 'https://' + str(request)
        else:
            verification_request = str(request)

        # Windows11, 
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        }

        try:
            # HTTP GET 요청을 통해 전달 받은 리다이렉션 정보.
            response = requests.get(
                url=verification_request,
                headers=headers,
                timeout=Config.REQUEST_TIMEOUT,
                allow_redirects=True
            )

            return request, response.url, response.status_code, ''
        except requests.exceptions.Timeout:
            return request, '', 'Request Timeout', f'응답 시간 초과: {Config.REQUEST_TIMEOUT}초'
        except requests.exceptions.RequestException as e:
            return request, '', 'Request Error', str(e)
        except requests.exceptions.ConnectionError:
            return request, '', 'Connection Error', '서버에 연결할 수 없습니다.'
