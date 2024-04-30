import streamlit as st
import google.generativeai as genai
import PyPDF2
from PIL import Image
import base64
import io

# Function to retrieve text from PDF
def retrieve_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

# Main function to orchestrate the process
def main():
    # PDF Path
    pdf_path = r"C:\my langchain project\leave_no_context_behind.pdf"

    # Model Name
    model_name = "gemini-1.5-pro-latest"

    # Read API key from file
    with open(r"C:\my langchain project\api_key.txt") as f:
        api_key = f.read()

    # Configure the API key
    genai.configure(api_key=api_key)

    # Set background image
    bg_image_path = r"C:\my langchain project\robotcute.jpeg"  # Replace with your image file path
    bg_image = Image.open(bg_image_path)

    # Convert image to base64
    buffered = io.BytesIO()
    bg_image.save(buffered, format="JPEG")
    bg_image_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Create Streamlit UI
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('data:image/jpeg;base64,{bg_image_base64}');
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create Streamlit UI
    st.snow()
    st.title(":rainbow[RAG System] 🤖")
    st.header('Advanced Q&A Bot Powered by Gemini Pro', divider='rainbow')
    

    # User input: Question
    question = st.text_input("Ask your question")

    if st.button("Generate Answers"):
        if question:
            # Retrieve text
            text = retrieve_text_from_pdf(pdf_path)

            # Concatenate PDF text with question prompt
            context = text + "\n\n" + question

            # Initialize the generative model
            ai = genai.GenerativeModel(model_name=model_name)

            # Generate response
            response = ai.generate_content(context)  

            # Display results
            st.subheader("Question:")
            st.write(question)
            st.subheader("Answer:")
            st.write(response.text)
        else:
            st.warning("Please enter your question.")

if __name__ == "__main__":
    main()
