import streamlit as st
import requests
import os
from typing import Optional

st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar configuration
st.sidebar.title("⚙️ Configuration")
backend_url = st.sidebar.text_input(
    "Backend URL",
    value="http://localhost:8000",
    help="Enter the FastAPI backend URL (e.g., https://your-backend.railway.app)"
)

llm_provider = st.sidebar.selectbox(
    "LLM Provider",
    ["openai", "anthropic", "ollama"],
    help="Select the LLM provider for code analysis"
)

st.sidebar.markdown("---")
st.sidebar.info(
    "🚀 **AI Code Reviewer v1.0**\n\n"
    "Analyze your code with AI-powered feedback.\n\n"
    "Features:\n"
    "- Code analysis & suggestions\n"
    "- RAG-based context retrieval\n"
    "- GitHub PR integration\n"
    "- Cost tracking"
)

# Main app
st.title("🤖 AI Code Reviewer")
st.markdown("Analyze your code with AI-powered feedback and intelligent suggestions")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📝 Code Analysis", "📊 RAG Pipeline", "💬 Feedback"])

# Tab 1: Code Analysis
with tab1:
    st.subheader("Analyze Your Code")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        code_input = st.text_area(
            "Paste your code here:",
            height=300,
            placeholder="# Python code\ndef my_function():\n    pass"
        )
    
    with col2:
        language = st.selectbox(
            "Language",
            ["python", "javascript", "typescript", "java", "cpp"],
            help="Programming language of the code"
        )
        
        file_path = st.text_input(
            "File path (optional)",
            placeholder="src/main.py",
            help="Path to the file for context"
        )
        
        analyze_button = st.button("🔍 Analyze Code", use_container_width=True)
    
    if analyze_button:
        if not code_input.strip():
            st.error("Please provide some code to analyze!")
        else:
            st.info("Analyzing your code...")
            
            try:
                # Call backend
                response = requests.post(
                    f"{backend_url}/analyze",
                    json={
                        "code": code_input,
                        "language": language,
                        "file_path": file_path,
                        "llm_provider": llm_provider
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display results
                    st.success("✅ Analysis Complete!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Issues Found", len(result.get("issues", [])))
                    with col2:
                        st.metric("Suggestions", len(result.get("suggestions", [])))
                    with col3:
                        st.metric("Quality Score", f"{result.get('quality_score', 0):.1%}")
                    
                    st.markdown("---")
                    
                    # Issues
                    if result.get("issues"):
                        st.subheader("🐛 Issues Found")
                        for i, issue in enumerate(result["issues"], 1):
                            with st.expander(f"Issue {i}: {issue.get('type', 'Unknown')}", expanded=False):
                                st.write(f"**Line:** {issue.get('line', 'N/A')}")
                                st.write(f"**Severity:** {issue.get('severity', 'medium')}")
                                st.write(f"**Message:** {issue.get('message', '')}")
                    
                    # Suggestions
                    if result.get("suggestions"):
                        st.subheader("💡 Suggestions")
                        for i, suggestion in enumerate(result["suggestions"], 1):
                            with st.expander(f"Suggestion {i}: {suggestion.get('title', 'Improvement')}", expanded=False):
                                st.write(suggestion.get("description", ""))
                                if suggestion.get("code_example"):
                                    st.code(suggestion["code_example"], language=language)
                    
                    # Summary
                    if result.get("summary"):
                        st.subheader("📋 Summary")
                        st.write(result["summary"])
                    
                    # Raw response
                    with st.expander("📊 Raw Response", expanded=False):
                        st.json(result)
                
                else:
                    st.error(f"Error: {response.status_code}")
                    st.write(response.text)
            
            except requests.exceptions.ConnectionError:
                st.error(f"❌ Cannot connect to backend at {backend_url}")
                st.info("Make sure the backend is running and the URL is correct.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Tab 2: RAG Pipeline
with tab2:
    st.subheader("Repository RAG Pipeline")
    st.write("Refresh your repository embeddings for context-aware code analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        repo_url = st.text_input(
            "Repository URL",
            placeholder="https://github.com/user/repo",
            help="GitHub repository URL"
        )
        
        refresh_button = st.button("🔄 Refresh RAG Index", use_container_width=True)
    
    if refresh_button:
        if not repo_url.strip():
            st.error("Please provide a repository URL!")
        else:
            st.info("Refreshing RAG index...")
            
            try:
                response = requests.post(
                    f"{backend_url}/rag/refresh",
                    json={"repo_url": repo_url},
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ RAG Index Refreshed!")
                    st.json(result)
                else:
                    st.error(f"Error: {response.status_code}")
                    st.write(response.text)
            
            except requests.exceptions.ConnectionError:
                st.error(f"❌ Cannot connect to backend at {backend_url}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Tab 3: Feedback
with tab3:
    st.subheader("Submit Code Review Feedback")
    st.write("Provide feedback on code analysis results")
    
    feedback_type = st.selectbox(
        "Feedback Type",
        ["helpful", "incorrect", "incomplete", "other"]
    )
    
    feedback_text = st.text_area(
        "Your Feedback:",
        placeholder="Tell us what you think about this analysis...",
        height=150
    )
    
    code_snippet = st.text_area(
        "Related Code Snippet (optional):",
        placeholder="Paste the code this feedback is about",
        height=100
    )
    
    if st.button("📤 Submit Feedback", use_container_width=True):
        if not feedback_text.strip():
            st.error("Please provide some feedback!")
        else:
            st.info("Submitting feedback...")
            
            try:
                response = requests.post(
                    f"{backend_url}/feedback",
                    json={
                        "type": feedback_type,
                        "text": feedback_text,
                        "code_snippet": code_snippet if code_snippet else None
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    st.success("✅ Feedback submitted successfully!")
                    st.balloons()
                else:
                    st.error(f"Error: {response.status_code}")
            
            except requests.exceptions.ConnectionError:
                st.error(f"❌ Cannot connect to backend at {backend_url}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center'>"
    "<p>Made with ❤️ using Streamlit + FastAPI</p>"
    "<p><small>GitHub: <a href='https://github.com/Ayushix17/ai-developer-review'>Ayushix17/ai-developer-review</a></small></p>"
    "</div>",
    unsafe_allow_html=True
)
