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


def generate_article():
    data = {"generate": "No further instructions"}

    response = requests.post(
        URL, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )
    return response.json()["answer"]


def app():
    st.title("Critical Thinking Bot")
    main, about, ex1 = st.tabs(["Enter Your Text", "How to Use", "Example 1"])

    with main:
        if "text_val" not in st.session_state:
            st.session_state["text_val"] = ""
        text_area_str = "Enter text from a news article, website, etc. for a critical reading analysis:"
        placeholder = st.empty()
        text_input = placeholder.text_area(
            text_area_str, value=st.session_state.text_val, height=400
        )

        if st.button("Generate Article", type="secondary"):
            with st.spinner("Please wait..."):
                article = generate_article()
                st.session_state.text_val = article.strip("\n")
                placeholder.text_area(
                    text_area_str, value=st.session_state.text_val, height=400
                )
            st.toast("Article has been generated!")

        if st.button("Submit", type="primary"):
            with st.spinner("Please wait..."):
                answer = query(text_input)
                st.write(answer)
            st.toast("Text has been analyzed!")

    with about:
        with open("how_to_use.txt", "r", encoding="utf-8") as f:
            st.write(f.read())

    with ex1:
        with open("ex1.txt", "r", encoding="utf-8") as f:
            st.write(f.read())


if __name__ == "__main__":
    app()
