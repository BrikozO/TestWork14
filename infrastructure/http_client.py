import httpx

http_client: httpx.Client = httpx.Client(follow_redirects=True, verify=True, timeout=10)
