import streamlit as st

def show_interrogation_page():
    # Check if game has started
    if not st.session_state.get("game_started", False):
        st.warning("Please start an investigation from the Home page first.")
        return
    
    # Check if mystery case exists
    if "mystery_case" not in st.session_state:
        st.warning("Please go to the briefing page first to generate your case.")
        return
    
    st.title("🔍 Interrogation Room")
    st.markdown("---")
    
    # Get the mystery case and game engine
    mystery_case = st.session_state["mystery_case"]
    game_engine = st.session_state["game_engine"]
    
    # Get the selected theme
    theme = st.session_state.get("selected_theme", "Unknown Theme")
    
    st.markdown(f"### Case: {theme}")
    st.markdown(f"Question suspects and witnesses to gather crucial information about the case.")
    
    # Display suspects
    st.markdown("### Available Suspects")
    suspects = mystery_case.suspects
    
    # Create tabs for each suspect
    if len(suspects) > 0:
        tab_names = [f"{suspect.name}" for suspect in suspects]
        tabs = st.tabs(tab_names)
        
        for i, (suspect, tab) in enumerate(zip(suspects, tabs)):
            with tab:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Name:** {suspect.name}")
                    st.markdown(f"**Occupation:** {suspect.occupation}")
                    st.markdown(f"**Age:** {suspect.age}")
                    st.markdown(f"**Personality:** {suspect.personality}")
                
                with col2:
                    st.markdown(f"**Alibi:** {suspect.alibi}")
                    st.markdown(f"**Potential Motive:** {suspect.motive}")
                
                st.markdown("---")
                st.markdown("### Question This Suspect")
                
                # Question input
                question = st.text_area(
                    f"What do you want to ask {suspect.name}?",
                    key=f"question_{i}",
                    placeholder="e.g., Where were you at the time of the crime? What was your relationship with the victim?"
                )
                
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    if st.button("Ask Question", key=f"ask_{i}", use_container_width=True):
                        if question.strip():
                            with st.spinner("Getting response..."):
                                response = game_engine.interrogate_suspect(suspect.name, question)
                                st.session_state[f"last_response_{i}"] = response
                
                # Display last response
                if f"last_response_{i}" in st.session_state:
                    st.markdown("### Response")
                    st.markdown(st.session_state[f"last_response_{i}"])
    
    # Quick navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Back to Briefing", use_container_width=True):
            st.session_state["current_page"] = "Briefing"
            st.rerun()
    
    with col2:
        if st.button("📋 Examine Evidence", use_container_width=True):
            st.session_state["current_page"] = "Evidence"
            st.rerun()
    
    with col3:
        if st.button("💡 Get Hints", use_container_width=True):
            st.session_state["current_page"] = "Hints"
            st.rerun()

if __name__ == "__main__":
    show_interrogation_page()