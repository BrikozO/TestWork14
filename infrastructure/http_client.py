import httpx

http_client: httpx.AsyncClient = httpx.AsyncClient(follow_redirects=True, verify=False, timeout=10)
