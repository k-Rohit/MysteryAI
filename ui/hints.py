import streamlit as st

def show_hints_page():
    # Check if game has started
    if not st.session_state.get("game_started", False):
        st.warning("Please start an investigation from the Home page first.")
        return
    
    # Check if mystery case exists
    if "mystery_case" not in st.session_state:
        st.warning("Please go to the briefing page first to generate your case.")
        return
    
    st.title("💡 Detective Hints")
    st.markdown("---")
    
    # Get the mystery case and game engine
    mystery_case = st.session_state["mystery_case"]
    game_engine = st.session_state["game_engine"]
    
    # Get the selected theme
    theme = st.session_state.get("selected_theme", "Unknown Theme")
    
    st.markdown(f"### Case: {theme}")
    st.markdown(f"Get hints to help guide your investigation when you're stuck.")
    
    # Hint difficulty selection
    st.markdown("### Choose Hint Difficulty")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🟢 Easy Hint", use_container_width=True):
            with st.spinner("Getting hint..."):
                hint = game_engine.get_hint("easy")
                st.session_state["current_hint"] = hint
                st.session_state["hint_difficulty"] = "Easy"
    
    with col2:
        if st.button("🟡 Medium Hint", use_container_width=True):
            with st.spinner("Getting hint..."):
                hint = game_engine.get_hint("medium")
                st.session_state["current_hint"] = hint
                st.session_state["hint_difficulty"] = "Medium"
    
    with col3:
        if st.button("🔴 Hard Hint", use_container_width=True):
            with st.spinner("Getting hint..."):
                hint = game_engine.get_hint("hard")
                st.session_state["current_hint"] = hint
                st.session_state["hint_difficulty"] = "Hard"
    
    # Display current hint
    if "current_hint" in st.session_state:
        st.markdown("---")
        st.markdown(f"### {st.session_state['hint_difficulty']} Hint")
        st.info(st.session_state["current_hint"])
    
    # Investigation progress
    st.markdown("---")
    st.markdown("### Investigation Tips")
    st.markdown("""
    **General Investigation Strategy:**
    
    1. **Start with the basics**: Question all suspects about their alibis and relationships
    2. **Cross-reference information**: Compare what different people tell you
    3. **Examine evidence carefully**: Look for connections between evidence and suspect statements
    4. **Look for inconsistencies**: People often reveal themselves through contradictions
    5. **Follow the money**: Many crimes have financial motives
    6. **Check timing**: Verify alibis and timeline details
    
    **Remember**: Every detail matters in solving a mystery!
    """)
    
    # Quick navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Back to Briefing", use_container_width=True):
            st.session_state["current_page"] = "Briefing"
            st.rerun()
    
    with col2:
        if st.button("🔍 Start Interrogation", use_container_width=True):
            st.session_state["current_page"] = "Interrogation"
            st.rerun()
    
    with col3:
        if st.button("📋 Examine Evidence", use_container_width=True):
            st.session_state["current_page"] = "Evidence"
            st.rerun()

if __name__ == "__main__":
    show_hints_page()