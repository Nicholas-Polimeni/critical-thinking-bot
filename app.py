import requests
import json
import streamlit as st

URL = r"https://us-east1-critical-thinking-bot-419021.cloudfunctions.net/critical-thinking-bot"


def query(text_input: str):
    data = {"query": text_input}
    response = requests.post(
        URL, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )
    return response.json()["answer"]


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
