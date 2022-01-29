def test_verify_headers_middleware(client):
    """
    GIVEN POST requests
    WHEN 'Content-Type' is not in headers
    THEN check the status and message of response
    """
    endpoints = [
        '/authentication/users',
        '/sales/purchases'
    ]
    mimetype = 'application/text'
    wrong_header = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    for endpoint in endpoints:
        req = client.post(endpoint)
        assert req.status == '400 BAD REQUEST'
        assert req.json['msg'] == 'Content-Type wrong or not set.'

        req = client.post(endpoint, headers=wrong_header)
        assert req.status == '400 BAD REQUEST'
        assert req.json['msg'] == 'Content-Type wrong or not set.'
