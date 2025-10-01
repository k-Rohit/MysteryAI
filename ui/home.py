# ui/home.py

import streamlit as st

def show_home_page():
    # Page configuration
    st.set_page_config(
        page_title="MysteryAI",
        page_icon="🕵️‍♂️",
        layout="centered",
    )

    # Main container
    st.markdown("""
        <div style="text-align: center;">
            <h1 style="font-size:48px; font-weight:bold;">🕵️‍♂️ MysteryAI</h1>
            <p style="font-size:18px; color:#555;">
                Step into the shoes of an Indian detective. Solve AI-generated mysteries set across India by interrogating suspects, analyzing evidence, and uncovering hidden clues.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Theme selection
    st.subheader("Choose a Mystery Theme")
    themes = [
        "Mumbai Underworld Mystery",
        "Delhi Political Scandal",
        "Bangalore Tech Startup Crime",
        "Kolkata Literary Society Murder",
        "Goa Beach Resort Mystery",
        "Rajasthan Palace Intrigue",
        "Kerala Backwater Mystery",
        "Punjab Farmhouse Crime"
    ]

    theme_choice = st.radio("Select a theme:", themes, index=0, key="theme_choice")

    st.markdown("---")

    # Start Game Button
    if st.button("🎯 Start Investigation",use_container_width=True):
        st.session_state["selected_theme"] = theme_choice
        st.session_state["game_started"] = True
        st.session_state["current_page"] = "Briefing"
        st.rerun()


    # Footer
    st.markdown("""
        <div style="text-align:center; color:#999; margin-top:50px;">
            © 2025 रहस्यAI - Developed by Rohit | भारत में बनाया गया
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
     show_home_page()