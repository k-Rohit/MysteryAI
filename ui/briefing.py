import streamlit as st
from mystery_engine import get_game_engine

def show_briefing_page():
    # Check if game has started
    if not st.session_state.get("game_started", False):
        st.warning("Please start an investigation from the Home page first.")
        return
    
    st.title("🕵️‍♂️ Case Briefing")
    st.markdown("---")
    
    # Get the selected theme
    theme = st.session_state.get("selected_theme", "Unknown Theme")
    
    # Check if API key is set
    if not st.session_state.get("openai_api_key"):
        st.error("⚠️ OpenAI API Key Required")
        st.info("Please enter your OpenAI API key in the sidebar to generate mystery cases.")
        st.markdown("""
        ### How to get your OpenAI API Key:
        1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
        2. Sign in or create an account
        3. Click "Create new secret key"
        4. Copy the key and paste it in the sidebar
        """)
        return
    
    # Initialize game engine and generate case if not exists
    if "mystery_case" not in st.session_state:
        try:
            with st.spinner("🔍 Generating your mystery case..."):
                game_engine = get_game_engine()
                # Map theme names to engine format
                theme_mapping = {
                    "Mumbai Underworld Mystery": "Mumbai underworld crime mystery with Bollywood connections",
                    "Delhi Political Scandal": "Delhi political corruption and scandal mystery", 
                    "Bangalore Tech Startup Crime": "Bangalore IT startup corporate crime mystery",
                    "Kolkata Literary Society Murder": "Kolkata intellectual literary society murder mystery",
                    "Goa Beach Resort Mystery": "Goa beach resort luxury crime mystery",
                    "Rajasthan Palace Intrigue": "Rajasthan royal palace intrigue and conspiracy mystery",
                    "Kerala Backwater Mystery": "Kerala backwaters tourism crime mystery",
                    "Punjab Farmhouse Crime": "Punjab agricultural farmhouse crime mystery"
                }
                engine_theme = theme_mapping.get(theme, "Mumbai underworld crime mystery with Bollywood connections")
                mystery_case = game_engine.generate_mystery(engine_theme)
                st.session_state["mystery_case"] = mystery_case
                st.session_state["game_engine"] = game_engine
        except Exception as e:
            st.error(f"Failed to generate mystery case: {str(e)}")
            st.info("Please check your OpenAI API key in the sidebar.")
            return
    
    # Get the mystery case
    mystery_case = st.session_state["mystery_case"]
    
    # Display case information
    st.markdown(f"### Case Theme: {theme}")
    st.markdown(f"You have been assigned to investigate this case. Review the information below and begin your investigation.")
    
    # Display case details
    st.markdown(f"## {mystery_case.title}")
    st.markdown(f"**{mystery_case.setting}**")
    st.markdown(f"**Crime:** {mystery_case.crime}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Victim Information")
        st.markdown(f"**{mystery_case.victim}**")
        
        st.markdown("### The Scene")
        st.markdown(mystery_case.initial_scene)
    
    with col2:
        st.markdown("### Suspects")
        for i, suspect in enumerate(mystery_case.suspects, 1):
            with st.expander(f"{i}. {suspect.name} - {suspect.occupation}, Age {suspect.age}"):
                st.markdown(f"**Occupation:** {suspect.occupation}")
                st.markdown(f"**Age:** {suspect.age}")
                st.markdown(f"**Personality:** {suspect.personality}")
                st.markdown(f"**Alibi:** {suspect.alibi}")
                st.markdown(f"**Potential Motive:** {suspect.motive}")
    
    st.markdown("---")
    
    # Investigation instructions
    st.markdown("""
    ### Your Investigation Tasks:
    
    1. **Interrogation**: Question suspects and witnesses to gather information
    2. **Evidence Analysis**: Examine physical evidence and crime scene details  
    3. **Hints**: Use available hints if you get stuck
    4. **Accusation**: Make your final accusation when you've solved the case
    
    **Remember**: Take your time, ask the right questions, and piece together the clues carefully. The truth is waiting to be discovered!
    """)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Start Interrogation", use_container_width=True):
            st.session_state["current_page"] = "Interrogation"
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
     show_briefing_page()