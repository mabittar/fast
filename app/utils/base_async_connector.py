import httpx

class BaseAsyncConnector:
    async def request_async(
        self,
        url=None,
        method=None,
        headers=None,
        payload=None,
        timeout=None,
        **kwargs
    ) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            if method == "GET":
                resp = await client.get(
                    url,
                    headers=headers,
                    timeout=timeout,
                )
            elif method == "POST":
                resp = await client.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=timeout,
                )
            elif method == "PUT":
                resp = await client.put(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=timeout,
                )
            elif method == "PATCH":
                resp = await client.patch(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=timeout,
                )
            elif method == "OPTIONS":
                resp = await client.options(
                    url,
                    headers=headers,
                    timeout=timeout,
                )
            elif method == "DELETE":
                resp = await client.delete(
                    url,
                    headers=headers,
                    timeout=timeout,
                )
            else:
                raise Exception("Undefined request method")
            return resp
