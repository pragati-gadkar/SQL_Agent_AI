import streamlit as st
import pandas as pd
from sql_agent_core import SQLAIAgent
import time

# Page configuration
st.set_page_config(
    page_title="SQL AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 10px 15px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .assistant-message {
        background-color: #f5f5f5;
        padding: 10px 15px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .sql-query {
        background-color: #263238;
        color: #aed581;
        padding: 10px;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    try:
        st.session_state.agent = SQLAIAgent()
        st.session_state.connected = True
        st.session_state.connection_error = None
    except Exception as e:
        st.session_state.connected = False
        st.session_state.connection_error = str(e)
        st.session_state.agent = None

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'show_sql' not in st.session_state:
    st.session_state.show_sql = True

# Sidebar
with st.sidebar:
    st.title("🤖 SQL AI Agent")
    st.markdown("---")
    
    # Connection status
    st.subheader("📡 Connection Status")
    if st.session_state.connected:
        conn_info = st.session_state.agent.get_connection_info()
        st.markdown(f"""
        <div class="success-box">
            ✅ Connected<br>
            <b>Database:</b> {conn_info['database']}<br>
            <b>Host:</b> {conn_info['host']}:{conn_info['port']}<br>
            <b>User:</b> {conn_info['user']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="error-box">
            ❌ Connection Failed<br>
            {st.session_state.connection_error}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Settings
    st.subheader("⚙️ Settings")
    st.session_state.show_sql = st.checkbox("Show SQL Queries", value=st.session_state.show_sql)
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    # Database Schema
    if st.session_state.connected:
        with st.expander("📊 Database Schema (Visual)", expanded=False):
            try:
                # Generate schema diagram image
                image_path = st.session_state.agent.generate_schema_image("schema_diagram.png")
                
                # Display the image
                st.image(image_path, caption="Database Schema Diagram", use_container_width=True)
                
                # Add legend
                st.markdown("""
                **Legend:**
                - 🟡 **Gold** = Primary Key (PK)
                - 🟢 **Green** = Foreign Key (FK)
                - 🔵 **Blue** = Regular Column
                """)
                
            except Exception as e:
                st.error(f"Error generating diagram: {e}")
                # Fallback to text schema
                schema_info = st.session_state.agent.get_schema_info()
                st.text(schema_info)
        
        with st.expander("📋 Database Schema (Text)", expanded=False):
            schema_info = st.session_state.agent.get_schema_info()
            st.text(schema_info)
    
    st.markdown("---")
    st.markdown("""
    ### Quick Examples
    - "Show me all tables"
    - "Count records in sales table"
    - "Show top 5 employees by salary"
    - "What's the average price?"
    """)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        Developed by: Pragati Gadkar<br>
        Tech Stack: Python, Streamlit, LangChain, Gemini AI
    </div>
    """, unsafe_allow_html=True)

# Main content
st.title("💬 SQL AgenticQuery")
st.markdown("Ask questions about your database in natural language with autonomous AI agents!")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            <b>👤 You:</b> {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f"""
        <div class="assistant-message">
            <b>🤖 Assistant:</b> {message["content"]}
        </div>
        """, unsafe_allow_html=True)
        
        # Show SQL query if enabled
        if st.session_state.show_sql and "sql_query" in message and message["sql_query"]:
            st.markdown(f"""
            <div class="sql-query">
                <b>SQL Query:</b><br>
                {message["sql_query"]}
            </div>
            """, unsafe_allow_html=True)
        
        # Show error if present
        if "error_log" in message and message.get("error_log"):
            st.markdown(f"""
            <div class="error-box">
                ⚠️ <b>SQL Error:</b> {message["error_log"]}
            </div>
            """, unsafe_allow_html=True)
        
        # Show query results if available
        if "query_results" in message and message["query_results"]:
            try:
                df = pd.DataFrame(message["query_results"])
                if not df.empty:
                    st.dataframe(df, use_container_width=True)
            except Exception as e:
                pass

# Chat input
if st.session_state.connected:
    question = st.chat_input("Ask a question about your database...")
    
    if question:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Show user message immediately
        st.markdown(f"""
        <div class="user-message">
            <b>👤 You:</b> {question}
        </div>
        """, unsafe_allow_html=True)
        
        # Process with agent
        with st.spinner("🔍 Analyzing your question..."):
            try:
                result = st.session_state.agent.ask(question)
                
                # Check if there was an error
                if result.get('error_log'):
                    response_text = f"I encountered an error while processing your request. The SQL query may have failed."
                else:
                    response_text = result.get('final_response', 'No response generated.')
                
                # Add assistant response
                assistant_message = {
                    "role": "assistant",
                    "content": response_text,
                    "sql_query": result.get('sql_query', ''),
                    "query_results": result.get('query_results', {}),
                    "error_log": result.get('error_log', '')
                }
                
                st.session_state.messages.append(assistant_message)
                
                # Rerun to show new messages
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
else:
    st.error("⚠️ Please check your database connection in the sidebar.")
    st.info("💡 Make sure your .env file contains the correct MySQL credentials.")
