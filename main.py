import streamlit as st
import bot
import textwrap

def reset_session_state():
    """Resets all session state variables related to product search."""
    st.session_state.product_name = ''
    st.session_state.db = None
    st.session_state.summary = ''
    st.session_state.questions_enabled = False

def main():
    st.title("Product Review Assistant")

    # Initialize session state
    if 'product_name' not in st.session_state:
        reset_session_state()

    # Product name input
    if not st.session_state.product_name:
        product_name = st.text_input("Enter the product name:")
        if st.button("Search"):
            reset_session_state()  # Reset everything before a new search
            st.session_state.product_name = product_name
            with st.spinner("Fetching and processing reviews..."):
                try:
                    # Pass the product_name to get_or_create_db
                    st.session_state.db = bot.get_or_create_db(product_name)
                    st.session_state.summary = bot.get_product_summary(st.session_state.db)
                    st.session_state.questions_enabled = True
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    reset_session_state()

    # Display summary and enable questions
    if st.session_state.product_name and st.session_state.summary:
        st.subheader(f"Summary for {st.session_state.product_name}")
        st.write(st.session_state.summary)
        
        if st.session_state.questions_enabled:
            question = st.text_input("Ask a question about the product:", key="question_input")
            
            if st.button("Ask", key="ask_button"):
                if question:
                    with st.spinner("Generating answer..."):
                        answer, _ = bot.get_response_from_query(st.session_state.db, question)
                        st.subheader("Answer:")
                        st.write(textwrap.fill(answer, width=85))
            
            # Keep showing the input box for new questions until "END" is pressed
            if st.button("END"):
                reset_session_state()
                st.experimental_set_query_params()  # Simulate a page reload
                st.success("You can now search for a new product.")

if __name__ == "__main__":
    main()
