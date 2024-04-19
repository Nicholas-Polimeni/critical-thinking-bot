import requests
import json
import streamlit as st

URL = r"https://us-east1-critical-thinking-bot-419021.cloudfunctions.net/critical-thinking-bot"


# force update
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
    main, about, ex1, ex2 = st.tabs(
        ["Enter Your Text", "How to Use", "Example 1", "Example 2"]
    )

    with main:
        if "text_val" not in st.session_state:
            st.session_state["text_val"] = ""

        st.write(
            """
                ### About
                 This application provides a critical reading analysis of a text. This analysis is intended to help you generate
                 your own questions and analysis.
                 
                 For more information about how to use the tool, see the "How to Use" tab.
                 
                 For walk-through examples, see the "Example 1" and "Example 2" tabs.
                 """
        )

        st.image("img_for_critical_thinking_bot.jpg", use_column_width=True)

        st.write("### Use the Tool ↓")
        st.info(
            """
            Note: if you do not want to provide your own text, but want to see how the tool works, press the "Generate Article" button.
            This will fill the textbox with an AI generated article. Please note that clicking the button multiple times may generate the
            same article to prevent unnecessary requests.
            """
        )

        text_area_str = "Enter text from a news article, website, etc. for a critical reading analysis:"
        placeholder = st.empty()
        text_input = placeholder.text_area(
            label="Paste or insert your text here",
            value=st.session_state.text_val,
            height=400,
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

        with open("how_to_use_2.txt", "r", encoding="utf-8") as f:
            st.info(f.read())

        with open("how_to_use_3.txt", "r", encoding="utf-8") as f:
            st.write(f.read())

    with ex1:

        with st.expander("Article Text", expanded=True):
            with open("ex1_text.txt", "r", encoding="utf-8") as f:
                st.write(f.read())
        with open("ex1.txt", "r", encoding="utf-8") as f:
            st.write(f.read())

    with ex2:
        with st.expander("Article Text", expanded=True):
            with open("ex1_text.txt", "r", encoding="utf-8") as f:
                st.write(f.read())

        with open("ex2.txt", "r", encoding="utf-8") as f:
            st.write(f.read())


if __name__ == "__main__":
    app()
