from requests.models import Response
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from requests.exceptions import ChunkedEncodingError, ConnectionError, ReadTimeout

@retry(
        stop=stop_after_attempt(5), 
        wait=wait_fixed(2), 
        retry=retry_if_exception_type((ChunkedEncodingError, ConnectionError)))
def safe_get(self, url, headers, cookies=None, allow_redirects=False, timeout=15) -> Response:
    try:
        response = self.session.get(url, headers=headers, cookies=cookies, allow_redirects=allow_redirects, timeout=timeout, stream=True)
    except ReadTimeout as err:
        print(err)
        self.create_session()
        response = self.session.get(url, headers=headers, cookies=cookies, allow_redirects=allow_redirects, timeout=timeout, stream=True)
        self.sid.write_sid(response.cookies.get_dict()['sid'])
    return response


@retry(
        stop=stop_after_attempt(5), 
        wait=wait_fixed(2), 
        retry=retry_if_exception_type((ChunkedEncodingError, ConnectionError)))
def safe_head(self, url, headers, cookies=None, allow_redirects=False, timeout=15) -> Response:
    try:
        response = self.session.head(url, headers=headers, cookies=cookies, allow_redirects=allow_redirects, timeout=timeout, stream=True)
    except ReadTimeout as err:
        print(err)
        self.create_session()
        response = self.session.head(url, headers=headers, cookies=cookies, allow_redirects=allow_redirects, timeout=timeout, stream=True)
        self.sid.write_sid(response.cookies.get_dict()['sid'])
    return response

@retry(
        stop=stop_after_attempt(10), 
        wait=wait_fixed(2), 
        retry=retry_if_exception_type((ReadTimeout)))
def safe_get_main_url(self, url, headers, cookies=None, allow_redirects=False, timeout=15) -> Response:
    if len(cookies['sid']) != 0:
        response = self.session.get(url, headers=headers, cookies=cookies, allow_redirects=True, timeout=timeout)
        if response.status_code == 200:
            self.session.cookies.update(cookies)
            self.sid.write_sid(self.session.cookies.get_dict())
            return response
        else:
            self.session.close()
    else:
        response = self.session.get(url, headers=headers, allow_redirects=True, timeout=timeout)
        if response.status_code == 200:
            self.session.cookies.update(response.cookies.get_dict())
            self.sid.write_sid(self.session.cookies.get_dict())
            return response

            
                

