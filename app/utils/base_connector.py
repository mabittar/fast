import requests

class BaseConnector:
    def request(
        self,
        url=None,
        method=None,
        headers=None,
        payload=None,
        **kwargs
    ) :
        if method == "GET":
            resp = requests.get(
                url,
                headers=headers,
                json=payload,
            )
        elif method == "POST":
            resp = requests.post(
                url,
                headers=headers,
                json=payload,
            )
        elif method == "PUT":
            resp = requests.put(
                url,
                headers=headers,
                json=payload,
            )
        elif method == "PATCH":
            resp = requests.patch(
                url,
                headers=headers,
                json=payload,
            )
        elif method == "OPTIONS":
            resp = requests.options(
                url,
                headers=headers,
                json=payload,
            )
        elif method == "DELETE":
            resp = requests.delete(
                url,
                headers=headers,
                json=payload,
            )
        else:
            raise Exception("Undefined request method")
        return resp

    
