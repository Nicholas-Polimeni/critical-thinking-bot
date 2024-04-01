import requests
import json
import streamlit as st


def query(text_input: str):
    url = "https://us-east4-legistlation-llm.cloudfunctions.net/llm-backend"
    data = {"query": text_input}
    response = requests.post(
        url, data=json.dumps(data), headers={"Content-Type": "application/json"}
    ).json()
    return response


def app():
    st.title("Critical Thinking Bot")
    main, about = st.tabs(["Home", "About"])

    with main:
        text_input = st.text_area("Enter your text here:")

        if text_input:
            with st.spinner("Please wait..."):
                answer = query(text_input)
                st.write(answer)

    with about:
        st.write("about...")


if __name__ == "__main__":
    app()
