import os
import functions_framework
from openai import OpenAI

API_KEY = os.environ.get("API_KEY", "Not set")
print(API_KEY)
client = OpenAI(api_key=API_KEY)

QUERY_PARAM = "query"


def call_openai(text_input: str):

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Given the above text, please generate critical reading questions. Please quote specific parts of the text.",
            },
            {"role": "user", "content": text_input},
        ],
    )

    return completion.choices[0].message


@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if not request_json:
        return "Status 404"

    if QUERY_PARAM in request_json:
        text_input = request_json[QUERY_PARAM]
    else:
        return "Status 400"

    return call_openai(text_input)
