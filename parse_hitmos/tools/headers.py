import fake_useragent


def get_headers():
    user = fake_useragent.UserAgent().random
    
    headers = {
        'User-Agent': user,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'DNT': '1',
        # 'Sec-GPC': '1',
        # 'Connection': 'keep-alive',
        # 'Upgrade-Insecure-Requests': '1',
        # 'Sec-Fetch-Dest': 'document',
        # 'Sec-Fetch-Mode': 'navigate',
        # 'Sec-Fetch-Site': 'none',
        # 'Sec-Fetch-User': '?1',
        # 'Priority': 'u=0, i',
        # 'Pragma': 'no-cache',
        # 'Cache-Control': 'no-cache',
    }
    return headers
