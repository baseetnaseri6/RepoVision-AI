import streamlit as st

st.set_page_config(
    page_title="AI GitHub Project Reviewer",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #f8fafc;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
}
[data-testid="stSidebar"] * {
    color: white;
}
.block-container {
    padding-top: 1.3rem;
    padding-bottom: 1rem;
}
.card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
}
.metric-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 16px;
    min-height: 125px;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
}
.metric-number {
    font-size: 32px;
    font-weight: 800;
    color: #0f172a;
}
.small-text {
    color: #64748b;
    font-size: 13px;
}
.title {
    color: #0f172a;
    font-size: 28px;
    font-weight: 800;
}
.badge-high {
    background: #fee2e2;
    color: #dc2626;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 12px;
}
.badge-low {
    background: #dbeafe;
    color: #2563eb;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🤖 AI GitHub<br>Project Reviewer", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Dashboard")
    st.markdown("🏠 Repository Review")
    st.markdown("🧠 Code Quality")
    st.markdown("🛡️ Security Scan")
    st.markdown("📁 File Structure")
    st.markdown("📄 README Review")
    st.markdown("---")
    st.markdown("📊 Metrics")
    st.markdown("⚠️ Issues")
    st.markdown("✅ Recommendations")

st.markdown('<div class="title">AI GitHub Project Reviewer</div>', unsafe_allow_html=True)
st.markdown('<div class="small-text">Analyze GitHub repositories with professional code, security and documentation insights.</div>', unsafe_allow_html=True)

st.write("")

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### Analyze a GitHub Repository")
col_input, col_btn = st.columns([5, 1])
with col_input:
    repo_url = st.text_input(
        " ",
        placeholder="https://github.com/username/repository",
        label_visibility="collapsed"
    )
with col_btn:
    st.button("Start Review")
st.markdown('<div class="small-text">Enter any public GitHub repository URL to get started.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

st.markdown("#### Project Overview")
m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    st.markdown('<div class="metric-card"><b>Overall Score</b><div class="metric-number">85</div><span class="small-text">/100 Very Good</span></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-card"><b>Code Quality</b><div class="metric-number">82</div><span class="small-text">/100 Good</span></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-card"><b>Security</b><div class="metric-number">78</div><span class="small-text">/100 Needs Improvement</span></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="metric-card"><b>Documentation</b><div class="metric-number">88</div><span class="small-text">/100 Excellent</span></div>', unsafe_allow_html=True)
with m5:
    st.markdown('<div class="metric-card"><b>Project Health</b><div class="metric-number">86</div><span class="small-text">/100 Very Good</span></div>', unsafe_allow_html=True)

st.write("")

c1, c2, c3 = st.columns([1.2, 1.2, 1.5])

with c1:
    st.markdown("""
    <div class="card">
        <h4>Repository Information</h4>
        <p><b>Repository:</b> octocat/Hello-World</p>
        <p><b>Language:</b> Python</p>
        <p><b>Stars:</b> 1,234</p>
        <p><b>Forks:</b> 567</p>
        <p><b>Size:</b> 2.4 MB</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <h4>Score Breakdown</h4>
        <p>Code Quality ████████░░ 82%</p>
        <p>Security ███████░░░ 78%</p>
        <p>Docs █████████░ 88%</p>
        <p>Health ████████░░ 86%</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
        <h4>Top Issues Found</h4>
        <p>🔴 Hardcoded secrets detected <span class="badge-high">High</span></p>
        <p>🔴 Missing input validation <span class="badge-high">High</span></p>
        <p>🟡 Large file detected <span class="badge-low">Medium</span></p>
        <p>🔵 Missing .gitignore file <span class="badge-low">Low</span></p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

r1, r2 = st.columns([2, 1])

with r1:
    st.markdown("""
    <div class="card">
        <h4>Recommendations</h4>
        <p>✅ Add input validation to prevent security vulnerabilities</p>
        <p>✅ Remove hardcoded secrets and use environment variables</p>
        <p>✅ Add unit tests to improve code coverage</p>
        <p>✅ Optimize large files and consider using Git LFS</p>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown("""
    <div class="card">
        <h4>File Type Distribution</h4>
        <p>🟣 Python — 45.2%</p>
        <p>🔵 Markdown — 20.1%</p>
        <p>🟢 JavaScript — 15.3%</p>
        <p>🟡 JSON — 10.2%</p>
    </div>
    """, unsafe_allow_html=True)
