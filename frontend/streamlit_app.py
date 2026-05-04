import os

import requests
import streamlit as st


st.set_page_config(page_title="AI Developer Review", layout="wide")
default_backend_hostport = os.getenv("BACKEND_HOSTPORT")
default_api_url = f"http://{default_backend_hostport}" if default_backend_hostport else "http://localhost:8000"
API_URL = st.sidebar.text_input("Backend URL", value=default_api_url)
st.title("AI Developer Review")
st.caption("Minimal MVP for pasted-code review")

tab_analyze, tab_history = st.tabs(["Analyze", "History"])

with tab_analyze:
    language = st.selectbox("Language", ["python", "javascript", "typescript"])
    context = st.text_area("Context (optional)", placeholder="Coding standards or repository notes")
    code = st.text_area("Code", height=320, placeholder="Paste code here")

    if st.button("Run Review", use_container_width=True):
        if not code.strip():
            st.error("Code is required.")
        else:
            response = requests.post(
                f"{API_URL}/analyze",
                json={"code": code, "language": language, "context": context or None},
                timeout=60,
            )
            if response.ok:
                result = response.json()
                st.success(result["summary"])
                col1, col2, col3 = st.columns(3)
                col1.metric("Findings", len(result["findings"]))
                col2.metric("Latency", f'{result["latency_ms"]} ms')
                col3.metric("Cost", f'${result["cost_usd"]:.6f}')

                for finding in result["findings"]:
                    with st.expander(f'{finding["severity"].upper()}: {finding["title"]}', expanded=False):
                        st.write(finding["description"])
                        if finding.get("line_number"):
                            st.caption(f'Line {finding["line_number"]}')
                        if finding.get("suggestion"):
                            st.code(finding["suggestion"])
            else:
                st.error(response.text)

with tab_history:
    if st.button("Refresh History", use_container_width=True):
        st.rerun()

    try:
        response = requests.get(f"{API_URL}/analyses", timeout=30)
        if response.ok:
            rows = response.json()
            if not rows:
                st.info("No analyses saved yet.")
            for row in rows:
                with st.expander(f'#{row["id"]} {row["language"]} - {row["summary"]}', expanded=False):
                    st.write(f'Latency: {row["latency_ms"]} ms')
                    st.write(f'Cost: ${row["cost_usd"]:.6f}')
                    detail = requests.get(f'{API_URL}/analyses/{row["id"]}', timeout=30)
                    if detail.ok:
                        data = detail.json()
                        st.code(data["input_code"], language=data["language"])
                        for finding in data["findings"]:
                            st.write(f'- **{finding["severity"]}** {finding["title"]}: {finding["description"]}')
        else:
            st.error("Could not load analysis history.")
    except requests.RequestException:
        st.info("Start the backend to load saved analysis history.")
