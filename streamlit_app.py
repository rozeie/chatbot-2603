import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("✈️ 여행 도우미 챗봇")
st.write(
    "여행 계획, 관광지 추천, 현지 문화, 숙소, 맛집 등 여행에 관한 모든 것을 물어보세요! "
    "이 챗봇을 사용하려면 OpenAI API 키가 필요합니다. "
    "[여기](https://platform.openai.com/account/api-keys)에서 발급받을 수 있어요."
)

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("OpenAI API 키를 입력하면 여행 도우미와 대화할 수 있어요!", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 여행 전문가 시스템 프롬프트
    SYSTEM_PROMPT = {
        "role": "system",
        "content": (
            "당신은 전문 여행 플래너입니다. "
            "여행지 추천, 일정 계획, 항공권·숙소 팁, 현지 음식, 문화, 비자, 날씨, 예산 등 "
            "여행과 관련된 모든 질문에 친절하고 상세하게 답변해주세요. "
            "여행과 무관한 질문에는 '저는 여행 관련 질문만 답변할 수 있어요 😊'라고 안내해주세요. "
            "한국어로 대화하며, 이모지를 적절히 활용해 친근하게 답변해주세요."
        )
    }

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 대화 기록 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("여행지, 일정, 맛집 등 무엇이든 물어보세요! 🌍"):

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 시스템 프롬프트 + 대화 기록을 함께 전달
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[SYSTEM_PROMPT] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})