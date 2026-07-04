# Polished AgentPassport Streamlit UI
# Replace app/app.py with this file.

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
# pyrefly: ignore [missing-import]
import streamlit as st

from pipeline import run_pipeline
from blockchain.blockchain import account
from dashboard.dashboard import (
    get_dashboard_data,
    get_badges,
    get_performance_history,
)

st.set_page_config(page_title="AgentPassport", page_icon="🛂", layout="wide")

MODELS = {
    "⚡ Gemini 2.5 Flash":"gemini-2.5-flash",
    "🧠 Gemini 2.5 Pro":"gemini-2.5-pro",
    "🚀 Gemini 3.5 Flash":"gemini-3.5-flash",
    "Gemini 2.0 Flash":"gemini-2.0-flash",
    "Gemini 2.0 Flash Lite":"gemini-2.0-flash-lite",
}

dashboard = get_dashboard_data(account.address)

with st.sidebar:
    st.title("🛂 AgentPassport")
    st.caption("AI Credential Platform")
    st.divider()
    st.write("**Wallet**")
    st.code(account.address)
    st.divider()
    st.metric("Tasks", dashboard["tasks_completed"])
    st.metric("Average", dashboard["average_score"])
    st.metric("Level", dashboard["level"])
    st.metric("Trust", dashboard["trust_score"])
    st.divider()
    st.markdown("### Workflow")
    st.markdown("""
📝 Task

⬇️

🤖 Worker

⬇️

⚖️ Judge

⬇️

⛓️ Monad

⬇️

📊 Passport
""")

st.title("🛂 AgentPassport")
st.caption("AI-powered credentials stored permanently on Monad Blockchain.")
st.divider()

tab1, tab2 = st.tabs(["🚀 Run Agent","📊 Dashboard"])

with tab1:
    c1,c2=st.columns([2,1])
    with c1:
        task=st.text_area("Task",height=170,placeholder="Ask the AI to perform any task...")
    with c2:
        model=MODELS[st.selectbox("Gemini Model", list(MODELS.keys()))]
        run=st.button("🚀 Generate & Verify",use_container_width=True)

    if run:
        if not task.strip():
            st.warning("Enter a task.")
        else:
            with st.spinner("Running workflow..."):
                result=run_pipeline(task,model)

            if result["success"]:
                st.success("Credential successfully generated!")

                with st.expander("🤖 Worker Output",expanded=True):
                    st.write(result["output"])

                st.subheader("⚖️ Judge")
                s=result["score"]
                a,b=st.columns([1,1])
                a.metric("Score",f"{s}/100")
                if s>=90:
                    b.success("Excellent")
                elif s>=75:
                    b.info("Good")
                else:
                    b.warning("Needs Improvement")
                st.progress(s/100)

                with st.expander("Judge Feedback"):
                    st.write(result["feedback"])

                st.success("✔ Permanently recorded on Monad")

                st.info("Immutable • Publicly Verifiable • Timestamped")

                st.code(result["tx_hash"])

                explorer_url = (
                    f"https://testnet.monadvision.com/tx/0x{result['tx_hash']}"
                )

                st.link_button(
                    "🔗 View on Monad Explorer",
                    explorer_url,
                )
            else:
                st.error(result["error"])

with tab2:
    dashboard=get_dashboard_data(account.address)

    st.subheader("Overview")
    r1=st.columns(3)
    with r1[0]:
        with st.container(border=True):
            st.metric("Tasks Completed",dashboard["tasks_completed"])
    with r1[1]:
        with st.container(border=True):
            st.metric("Average Score",dashboard["average_score"])
    with r1[2]:
        with st.container(border=True):
            st.metric("Highest Score",dashboard["highest_score"])

    r2=st.columns(3)
    with r2[0]:
        with st.container(border=True):
            st.metric("Trust Score",dashboard["trust_score"])
    with r2[1]:
        with st.container(border=True):
            st.metric("Level",dashboard["level"])
    with r2[2]:
        with st.container(border=True):
            st.metric("Status",dashboard["status"])

    st.subheader("🏅 Badges")
    badges=get_badges(account.address)
    cols=st.columns(len(badges))
    for col,badge in zip(cols,badges):
        with col:
            with st.container(border=True):
                st.markdown(f"## {badge['icon']}")
                st.write(badge["name"])
                if badge["earned"]:
                    st.success("Earned")
                else:
                    st.caption("Locked")

    st.subheader("📈 Performance History")
    history=get_performance_history(account.address)
    if history:
        df=pd.DataFrame(history)
        if "timestamp" in df.columns:
            df["timestamp"]=pd.to_datetime(df["timestamp"]).dt.strftime("%d %b %H:%M")
        if "task" in df.columns:
            df["task"]=df["task"].str.slice(0,60)
        st.dataframe(df,use_container_width=True,hide_index=True)
    else:
        st.info("No history found.")

st.divider()
st.caption("Built for Monad Blitz Hackathon • Powered by Gemini • Monad • Streamlit")
