import os
import functions_framework
import anthropic

API_KEY = os.environ.get("API_KEY")
client = anthropic.Anthropic(api_key=API_KEY)

QUERY_PARAM = "query"
GEN_PARAM = "generate"


def call_ai(text_input: str, query: bool):

    SYSTEM = ""
    path = None
    if query:
        path = "system_prompt.txt"
    else:
        path = "gen_prompt.txt"
    with open(path, "r") as f:
        SYSTEM = f.read()

    message = client.messages.create(
        model="claude-instant-1.2",
        max_tokens=1000,
        temperature=0.0,
        system=SYSTEM,
        messages=[{"role": "user", "content": text_input}],
    )

    print(message.content[0].text)
    return message.content[0].text


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
    print(request)
    request_json = request.get_json()
    print(request_json)

    if not request_json:
        return "Status 404"

    query = True
    if QUERY_PARAM in request_json:
        text_input = request_json[QUERY_PARAM]
    elif GEN_PARAM in request_json:
        text_input = request_json[GEN_PARAM]
        query = False
    else:
        return "Status 400"

    resp = call_ai(text_input, query)
    return {"answer": resp}
