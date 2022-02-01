import requests


class BoticarioCashback:
    """
    Integration with Boticario's credits API
    """
    @classmethod
    def get_boticario_credits(cls, cpf):
        req = requests.get(f'https://mockbin.org/bin/91584f88-ba1f-45c0-bab1-3bbd37113460?cpf={cpf}')
        if req.status_code == 200:
            return req.json()['credit']
        return None
