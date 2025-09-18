import httpx

http_client: httpx.Client = httpx.Client(follow_redirects=True, verify=False, timeout=10)
