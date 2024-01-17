import os
from unittest.mock import patch
from moto import mock_dynamodb

COGINTO_USERNAME = "test@example.com"
COGINTO_PASSWORD = "NewPassword456!"


@patch.dict(os.environ, {"DISABLE_XRAY": "True", "EVENT_BUS_ARN": ""})
def test_search_works(setup_dynamodb_collection_with_items):
    from functions.Search.app import lambda_handler

    event = {
        "headers": {
            "token": "eyJraWQiOiJ2TlhZTWpKUWRmU0FSaEpSSWJsVFloSHNWM0N1TVdyR096T05xQnBsdnJJPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJlYzcxZGQ4ZC1hZWU5LTQwYjEtYWM4YS03MWMzNDdjNjE3NmIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfNmRMVXg4TW1BIiwiY29nbml0bzp1c2VybmFtZSI6ImVjNzFkZDhkLWFlZTktNDBiMS1hYzhhLTcxYzM0N2M2MTc2YiIsIm9yaWdpbl9qdGkiOiJhZTBiNjk0NS0yNmRiLTQ0ODUtOThjMC1jODBlNzM3YmVjMzEiLCJhdWQiOiI3dms3NzAzbHJ1MGxiMjVxcWhvMzkzazkyaCIsImV2ZW50X2lkIjoiY2ExOGQyYzItNjc3Mi00OTE1LTliNzgtZTAxMDYwOTJjMTU2IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3MDU1MDIyMTksImV4cCI6MTcwNTUwNTgxOSwiaWF0IjoxNzA1NTAyMjE5LCJqdGkiOiIwNzk5NDVkMS0zY2UxLTQ4ZGQtODgzOC02OGFkMzIwYWI0NDAiLCJlbWFpbCI6ImpvcmR5LmJyb25vd2lja2lAc3R1ZGVudC5odS5ubCJ9.QKXHTHHA95QdyzgJWoC99EWQ6O8G-0DQ9-GQqtPEoK-raC78lk4rqZ_zOU8PYu_UWwsJxdqHgCCwyIsdE0-eN67utOm0sLmt089BfV_4jzjAUnUa6p0DE92AmL2wpPUib53P-0rFP3o9kzPvs8oVHwo_Bxfgr5C8wqZukbDtESns-c16snpX56MqgUmh_CvEGCYyDSAHu0RNEn3SeUs8x6navANKwEzVsFT3RKi2dgkOmNParK7W2FKAB2cAjnMET6zJ-hEBrJi8iKbGj_gnxHLlCnRbA4HHtneo4eAgBX9b5fMHvh7q-YtD95x-fA-vPkUHTRT_XDRkHE9JiQNL3A"
        },
        "queryStringParameters": {"q": "doctor"},
    }

    # Act
    result = lambda_handler(event, None)

    # Assert
    expected_output = {
        "statuscode": 200,
        "body": {
            "Items": [
                {
                    "UserId": "123",
                    "UserName": "JohnDoe",
                    "Age": "30",
                    "Email": "john.doe@example.com",
                },
                {
                    "UserId": "456",
                    "UserName": "JaneSmith",
                    "Age": "25",
                    "Email": "jane.smith@example.com",
                },
            ],
        },
    }

    assert result == expected_output


@patch.dict(os.environ, {"DISABLE_XRAY": "True", "EVENT_BUS_ARN": ""})
def test_search_not_found(setup_dynamodb_collection):
    from functions.Search.app import lambda_handler

    # Arrange
    event = {
        "headers": {"token": "valid_id_token"},
        "queryStringParameters": {"q": "invalid"},
    }

    # Act
    result = lambda_handler(event, None)

    # Assert
    expected_output = {
        "statuscode": 404,
        "body": {"message": "Not found"},
        "headers": {
            "Content-Type": "application/json",
        },
    }

    assert result == expected_output
