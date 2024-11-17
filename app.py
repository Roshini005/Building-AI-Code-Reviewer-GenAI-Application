import streamlit as st
import google.generativeai as genai

# Set up Google Generative AI API with your API key
genai.configure(api_key="AIzaSyBWfxxbjYaRWmD-HAztP4gtRfMU1TxQJxg")  # Use your actual API key

# Set up the layout of the app
st.set_page_config(page_title="AI Code Companion", layout="wide")

# Title and description of the app
st.title("👨‍💻 Code Assistant & AI Chat Buddy 🤖")
st.markdown("""
    **Welcome to Code Assistant & AI Chat Buddy**! 🌟  
    You can either ask coding questions or share your Python code, and our AI will help you with advice, explanations, and suggestions.
""")

# Initialize conversation history to keep track of chat
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Section for user to type their code or question
st.subheader("💬 Your Coding Playground: Type Your Code or Question!")

# Large input box for the user to enter their query or code
user_query = st.text_area(
    "Type your Python code or a question here:",
    height=250,
    max_chars=2000,
    placeholder="E.g., 'How do I implement recursion in Python?' or paste your code here..."
)

# Submit button 
if st.button("🔍 Ask AI for Help"):
    if user_query.strip():  # Check if input is not empty
        # Initialize the Generative AI model
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        
        # Prepare the user's message to send to the AI
        user_message = {
            "role": "user",  # User's message role
            "parts": [
                {
                    "text": user_query  # The actual input from the user
                }
            ]
        }

        # Save the user's message to session history
        st.session_state.conversation_history.append(user_message)
        
        # Guide the AI to focus on giving clear, helpful answers
        guidance = """
        You are an AI Assistant for Python programming. Help the user with code issues, suggestions, or answers to questions.
        If the user provides code, analyze it and suggest improvements. If they ask a question, provide a clear answer.
        """

        # Add guidance to session history for context
        st.session_state.conversation_history.append({
            "role": "user",
            "parts": [{"text": guidance}]
        })

        # Get the AI's response based on the conversation history
        chat_session = model.start_chat(history=st.session_state.conversation_history)
        ai_response = chat_session.send_message(user_query)

        # Save the AI's response
        ai_message = {
            "role": "model",  # AI's message role
            "parts": [
                {
                    "text": ai_response.text  # The AI's response
                }
            ]
        }

        # Add the AI's response to session history
        st.session_state.conversation_history.append(ai_message)

        # Show the AI's response to the user
        st.subheader("🔍 Here’s What I Found for You:")
        if user_query.strip().startswith("def") or "import" in user_query:
            st.markdown("### 🛠️ **Code Review & Suggestions**:")
            st.code(ai_response.text)  # Show the AI's code review as formatted code
        else:
            st.markdown("### 💬 **Your AI Chat Buddy Says**:")
            st.write(ai_response.text)  # Show the AI's response as plain text

        # Optional feedback section for the user
        st.markdown("💬 **Tell Us What You Think About This Response!**")
        user_feedback = st.text_input("Your feedback (optional):", max_chars=300)

        # If feedback is given, save it in session history
        if user_feedback:
            st.session_state.conversation_history.append({
                "role": "user",
                "parts": [{"text": f"Feedback: {user_feedback}"}]
            })
            st.write("Thank you for your feedback! It helps improve our responses.")

        st.markdown("---")
        st.markdown("🔄 Want to try again? Modify your input above and click the button!")

    else:
        st.warning("⚠️ Please enter something before clicking the button!")

# Option to show conversation history (useful for debugging or reference)
if st.checkbox("Show Conversation History (for debugging or reference)"):
    st.write(st.session_state.conversation_history)
