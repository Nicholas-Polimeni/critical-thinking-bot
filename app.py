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
    main, about = st.tabs(["Enter Your Text", "How to Use"])

    with main:
        with st.form("input"):
            text_input = st.text_area(
                "Enter text from a news article, website, etc. for a critical reading analysis:"
            )

            submitted = st.form_submit_button("Submit")
            if submitted:
                with st.spinner("Please wait..."):
                    answer = query(text_input)
                    st.write(answer)
                    st.toast("Text has been analyzed!")

    with about:
        st.write("about...")


if __name__ == "__main__":
    app()
