# main.py
import streamlit as st
import os
from style_transfer import apply_style
from PIL import Image

STYLE_IMAGES_DIR = "data/styles/"
STYLE_OPTIONS = {
    "Van Gogh": "van_gogh.jpg",
    "Monet": "monet.jpg",
    "Picasso": "picasso.jpg",
    "Kandinsky": "kandinsky.jpg",
    "Dali": "dali.jpg"
}

st.set_page_config(page_title="스타일 변환기", layout="centered")
st.title("AI 화풍 스타일 변환기")
st.markdown("업로드한 이미지를 선택한 화풍 스타일로 변환해드립니다.")

# 1. 콘텐츠 이미지 업로드
uploaded_file = st.file_uploader("이미지를 업로드하세요 (JPG/PNG)", type=["jpg", "jpeg", "png"])

# 2. 스타일 선택
style_name = st.selectbox("적용할 화풍을 선택하세요", list(STYLE_OPTIONS.keys()))

# 3. 변환 실행
if uploaded_file is not None:
    input_path = "data/input.jpg"
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    st.image(Image.open(input_path), caption="📥 원본 이미지", use_column_width=True)

    if st.button("스타일 변환 실행"):
        style_path = os.path.join(STYLE_IMAGES_DIR, STYLE_OPTIONS[style_name])
        output_path = "data/output.jpg"

        with st.spinner("스타일 적용 중..."):
            apply_style(input_path, style_path, output_path)

        st.success("스타일 변환 완료!")
        st.image(Image.open(output_path), caption="변환된 이미지", use_column_width=True)
