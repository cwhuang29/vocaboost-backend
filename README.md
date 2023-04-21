# VocaBoost - Backend

VocabularyBoost (VocaBoost) helps you improve GRE vocabulary in an effective way.

View VocaBoost official website on [here](https://www.vocabularyboost.com/).

Install VocaBoost extension on [Chrome Web Store](https://chrome.google.com/webstore/detail/gre-vocabulary-highlighte/gfkmbmplhjdoejicgmaldndkcnnpplho).

Install VocaBoost app on [App Store](https://apps.apple.com/app/vocabboost/id6447704480).

## Commands

- Run the server: `uvicorn main:app --reload`

## Setup

1. Setup python environment

    ```bash
    pip3 install virtualenv
    python3 -m virtualenv venv
    source venv/bin/activate
    pip install fastapi "uvicorn[standard]" SQLAlchemy pymysql email-validator "python-jose[cryptography]" websockets
    ```

2. Check `config.py` and setup all necessary env variables

## Structure

- `routers/`: routers of the backend apis
- `handlers/`: handlers for incoming network requests
- `structs/`
    - `requests/`: format of network requests’ body
    - `models/`: ORM classes (interact with the database)
    - `schemas/`: data validation, conversion, and documentation classes. Defines more or less a "schema" (a valid data shape)

    Note: **SQLAlchemy** uses the term "**model**" to refer to these classes and instances that interact with the database. **Pydantic** also uses the term "**model**" (refer to **schema** here) to refer to something different, the data validation, conversion, and documentation classes and instances.

- `databases/`: interact with the data in the database
- `utils/`: utilities and helper functions


## Notes

### JWT

Get JWT secret key by `openssl rand -hex 32`, output looks like `9e283bd0313d49ca307f2fdc4b9d4ad8ae8cc63a0d14406791b2c4ce54bf860d`

### API Examples

- Login

    ```bash
    curl -X 'POST' \
      'http://localhost:8000/v1/login' \
      -H 'X-VH-Source: mobile' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "loginMethod": 1,
      "detail": {
        "email": "test123@test.com",
        "firstName": "Jack",
        "lastName": "ABC",
        "scopes": "[https://www.googleapis.com/auth/userinfo.email]",
        "serverAuthCode": "",
        "avatar": "https://wlh3.googleusercontent.com/a/AH8GmiVYK36"
      },
      "timeStamp": "2023-04-03T01:34:47.594Z"
    }'
    # Response (success)
    # {
    #   "accessToken":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkNjRiZmZkNC0zNTE1LTQxN2YtODgxOS0yYzI2MzEwZjlhODIiLCJtZXRob2QiOjEsImVtYWlsIjoidGVzdDEyM0Bmd2FzLmNvbSIsImV4cCI6MTY4MDQ5MDMwNX0.Od8UDNFWpm-O5-UbLeiH4lmIOYMehSVEIZ3y0nrq_XQ",
    #   "tokenType":"bearer"
    # }
    # Response (failed)
    # {"detail":{"errHead":"Login type is not supported","errBody":""}}
    ```

- Logout

    ```bash
    # Logout
    jwt=<accessToken from response>
    curl -X 'POST' \
      'http://localhost:8000/v1/logout' \
      -H 'accept: application/json' \
    	-H 'X-VH-Source: mobile' \
      -H "Authorization: Bearer ${jwt}"
    # Response
    # {"result":"success"}
    ```

- Me (retrieve user’s profile data)

    ```bash
    jwt=<accessToken from response>
    curl -X 'GET' \
      'http://localhost:8000/v1/users/me' \
      -H 'accept: application/json' \
    	-H 'X-VH-Source: mobile' \
      -H "Authorization: Bearer ${jwt}"
    # Response (succeed)
    # {
    #   "uuid":"d64bffd4-3515-417f-8819-2c26310f9a82",
    #   "loginMethod":1,
    #   "firstName":"Jack",
    #   "lastName":"ABC",
    #   "createdAt":"2023-04-03T01:34:47.594000",
    #   "email":"test123@fwas.com",
    #   "avatar":"https://wlh3.googleusercontent.com/a/AH8GmiVYK36"
    # }
    # Response (error)
    # {"detail":{"errHead":"You are not allowed to perform this action","errBody":"You should login first"}}
    ```
