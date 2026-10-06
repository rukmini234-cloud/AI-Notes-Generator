import streamlit as st
from pypdf import PdfReader
from ollama import chat

st.set_page_config(
    page_title="AI Notes Generator",
    page_icon="📝",
    layout="wide"
)

st.title("📝 AI Notes Generator")
st.write("Upload a PDF or enter study material and generate clear notes using AI.")

# Sidebar
st.sidebar.header("⚙️ Note Settings")

note_format = st.sidebar.selectbox(
    "Select Note Format",
    [
        "Bullet Summary",
        "Detailed Notes",
        "Structured Outline",
        "Question and Answer",
        "Flashcards"
    ]
)

detail_level = st.sidebar.selectbox(
    "Select Detail Level",
    [
        "Concise",
        "Detailed"
    ]
)

# PDF Upload
st.subheader("📄 Upload Study Material")

uploaded_file = st.file_uploader(
    "Upload your PDF file",
    type=["pdf"]
)

pdf_text = ""

if uploaded_file is not None:

    try:
        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pdf_text += text + "\n"

        if pdf_text.strip():
            st.success(
                f"PDF uploaded successfully! Pages: {len(reader.pages)}"
            )

            with st.expander("👀 Preview PDF Text"):
                st.text(pdf_text[:5000])

        else:
            st.warning(
                "Could not extract text from this PDF. "
                "It may be a scanned/image-based PDF."
            )

    except Exception as e:
        st.error("Error reading PDF.")
        st.code(str(e))


# Manual text input
st.subheader("📝 Or Enter Study Material")

manual_text = st.text_area(
    "Paste your study material here",
    height=250,
    placeholder="Paste your lecture notes or study material..."
)


# Generate Notes
if st.button("🚀 Generate Notes", type="primary"):

    # Choose PDF text or manual text
    if pdf_text.strip():
        study_material = pdf_text

    elif manual_text.strip():
        study_material = manual_text

    else:
        st.warning(
            "Please upload a PDF or enter study material."
        )
        st.stop()

    prompt = f"""
You are an AI study notes generator.

Convert the following study material into:
{note_format}

Detail level:
{detail_level}

Follow these rules:

1. Use only information from the provided study material.
2. Do not invent facts.
3. Make the notes easy for students to understand.
4. Use clear headings and subheadings.
5. Highlight important concepts.
6. Include important definitions.
7. Include examples when they are present in the source.
8. Use bullet points where appropriate.
9. Make the output well organized.
10. Use Markdown formatting.

STUDY MATERIAL:

{study_material}
"""

    try:

        with st.spinner("🤖 AI is generating your notes..."):

            response = chat(
                model="llama3.2",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            notes = response["message"]["content"]

        st.success("✅ Notes generated successfully!")

        st.subheader("📚 Generated Notes")

        st.markdown(notes)

        # Download
        st.download_button(
            label="⬇️ Download Notes",
            data=notes,
            file_name="AI_Generated_Notes.md",
            mime="text/markdown"
        )

    except Exception as e:

        st.error("❌ Error while generating notes.")

        st.code(str(e))