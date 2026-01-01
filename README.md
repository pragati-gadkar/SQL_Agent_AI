# 🤖 SQL AgenticQuery

**SQL AgenticQuery** is a powerful, autonomous SQL AI Assistant that transforms natural language questions into precise database queries. Built with a multi-agent orchestration layer, it doesn't just generate SQL—it executes it, validates the results, and self-corrects if errors occur.

## 🚀 Key Features

- **Autonomous Orchestration**: Uses **LangGraph** to manage a multi-step workflow (Schema Fetching -> SQL Generation -> Execution -> Validation).
- **Self-Correction Loop**: Automatically detects SQL syntax errors and iteratively fixes them before presenting results to the user.
- **Visual Schema Explorer**: Dynamically generates visual ER diagrams from your live database metadata using **Pillow**.
- **Data Validation**: A dedicated "validator" node ensures that the final AI-generated response accurately reflects the data returned by the database.
- **Streamlit Interface**: A modern, interactive chat experience with real-time feedback and SQL code inspection.

## 🛠️ Tech Stack

- **AI Orchestration**: LangChain & LangGraph
- **LLM**: Google Gemini 1.5 Flash
- **Database**: MySQL with SQLAlchemy ORM
- **Frontend**: Streamlit
- **Data Handling**: Pandas

## 📋 Prerequisites

- Python 3.9+
- MySQL Server
- Google Gemini API Key

## ⚙️ Setup Instructions

1.  **Clone the Repository**
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Environment**:
    Create a `.env` file in the root directory:
    ```env
    GOOGLE_API_KEY=your_gemini_api_key_here
    MYSQL_USER=root
    MYSQL_PASSWORD=your_password
    MYSQL_HOST=localhost
    MYSQL_PORT=3306
    MYSQL_DATABASE=your_database_name
    ```

## 🚀 How to Run

### Run the Web Interface
```bash
streamlit run app.py
```

### Run the CLI Agent
```bash
python sql_agent_core.py
```

## 👤 Developer
**Pragati Gadkar**
Assistant specializing in AI-driven database automation.
