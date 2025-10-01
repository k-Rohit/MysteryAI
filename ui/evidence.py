import streamlit as st

def show_evidence_page():
    # Check if game has started
    if not st.session_state.get("game_started", False):
        st.warning("Please start an investigation from the Home page first.")
        return
    
    # Check if mystery case exists
    if "mystery_case" not in st.session_state:
        st.warning("Please go to the briefing page first to generate your case.")
        return
    
    st.title("📋 Evidence Analysis")
    st.markdown("---")
    
    # Get the mystery case and game engine
    mystery_case = st.session_state["mystery_case"]
    game_engine = st.session_state["game_engine"]
    
    # Get the selected theme
    theme = st.session_state.get("selected_theme", "Unknown Theme")
    
    st.markdown(f"### Case: {theme}")
    st.markdown(f"Examine physical evidence, documents, and forensic findings from the crime scene.")
    
    # Display evidence
    st.markdown("### Evidence Collection")
    evidence_list = mystery_case.evidence
    
    if len(evidence_list) > 0:
        # Create expandable sections for each piece of evidence
        for i, evidence in enumerate(evidence_list):
            with st.expander(f"🔍 {evidence.name} - Found at {evidence.location}"):
                st.markdown(f"**Description:** {evidence.description}")
                st.markdown(f"**Significance:** {evidence.significance}")
                
                # Button to get detailed analysis
                if st.button(f"🔬 Get Detailed Analysis", key=f"analyze_{i}"):
                    with st.spinner("Analyzing evidence..."):
                        analysis = game_engine.examine_evidence(evidence.name)
                        st.markdown("### Forensic Analysis")
                        st.text(analysis)
    else:
        st.info("No evidence available yet.")
    
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
        if st.button("💡 Get Hints", use_container_width=True):
            st.session_state["current_page"] = "Hints"
            st.rerun()

if __name__ == "__main__":
    show_evidence_page()