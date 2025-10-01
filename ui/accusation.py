import streamlit as st

def show_accusation_page():
    # Check if game has started
    if not st.session_state.get("game_started", False):
        st.warning("Please start an investigation from the Home page first.")
        return
    
    # Check if mystery case exists
    if "mystery_case" not in st.session_state:
        st.warning("Please go to the briefing page first to generate your case.")
        return
    
    st.title("⚖️ Make Your Accusation")
    st.markdown("---")
    
    # Get the mystery case and game engine
    mystery_case = st.session_state["mystery_case"]
    game_engine = st.session_state["game_engine"]
    
    # Get the selected theme
    theme = st.session_state.get("selected_theme", "Unknown Theme")
    
    st.markdown(f"### Case: {theme}")
    st.markdown(f"Based on your investigation, make your final accusation.")
    
    # Display suspects for selection
    st.markdown("### Select the Perpetrator")
    suspects = mystery_case.suspects
    
    if len(suspects) > 0:
        suspect_options = [f"{suspect.name} - {suspect.occupation}" for suspect in suspects]
        selected_suspect_idx = st.selectbox(
            "Who do you believe committed the crime?",
            range(len(suspects)),
            format_func=lambda x: suspect_options[x]
        )
        
        selected_suspect = suspects[selected_suspect_idx]
        
        # Explanation input
        st.markdown("### Explain Your Reasoning")
        explanation = st.text_area(
            "Provide your detailed explanation of why you believe this person is guilty:",
            placeholder="Include the evidence that led you to this conclusion, inconsistencies in their story, and how everything fits together...",
            height=150
        )
        
        # Submit accusation
        if st.button("🎯 Submit Accusation", use_container_width=True, type="primary"):
            if explanation.strip():
                with st.spinner("Evaluating your solution..."):
                    result = game_engine.submit_solution(selected_suspect.name, explanation)
                    
                    # Display results
                    st.markdown("---")
                    st.markdown("## 🎯 Investigation Results")
                    
                    if result["correct"]:
                        st.success("🎉 **CASE SOLVED!** 🎉")
                        st.balloons()
                    else:
                        st.error("❌ **Not quite right**")
                    
                    # Score and feedback
                    st.markdown(f"### Score: {result['score']}/100")
                    st.markdown("### Feedback:")
                    st.info(result["feedback"])
                    
                    # Missed clues
                    if result.get("missed_clues") and len(result["missed_clues"]) > 0:
                        st.markdown("### Important Clues You May Have Missed:")
                        for clue in result["missed_clues"]:
                            st.markdown(f"• {clue}")
                    
                    # Options after evaluation
                    st.markdown("---")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("🔄 Try Another Case", use_container_width=True):
                            # Clear current case data
                            keys_to_clear = ["mystery_case", "game_engine", "current_page"]
                            for key in keys_to_clear:
                                if key in st.session_state:
                                    del st.session_state[key]
                            st.session_state["current_page"] = "Briefing"
                            st.rerun()
                    
                    with col2:
                        if st.button("🏠 Back to Home", use_container_width=True):
                            # Reset entire game
                            for key in ["game_started", "selected_theme", "mystery_case", "game_engine", "current_page"]:
                                if key in st.session_state:
                                    del st.session_state[key]
                            st.rerun()
            else:
                st.warning("Please provide an explanation for your accusation.")
    
    # Investigation summary
    st.markdown("---")
    st.markdown("### Investigation Summary")
    st.markdown("**Available Suspects:**")
    for i, suspect in enumerate(suspects, 1):
        with st.expander(f"{i}. {suspect.name} - {suspect.occupation}, Age {suspect.age}"):
            st.markdown(f"**Occupation:** {suspect.occupation}")
            st.markdown(f"**Age:** {suspect.age}")
            st.markdown(f"**Personality:** {suspect.personality}")
            st.markdown(f"**Alibi:** {suspect.alibi}")
            st.markdown(f"**Potential Motive:** {suspect.motive}")
    
    st.markdown("**Evidence Collected:**")
    for i, evidence in enumerate(mystery_case.evidence, 1):
        st.markdown(f"{i}. **{evidence.name}** - Found at {evidence.location}")
    
    # Quick navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Back to Briefing", use_container_width=True):
            st.session_state["current_page"] = "Briefing"
            st.rerun()
    
    with col2:
        if st.button("🔍 Review Interrogations", use_container_width=True):
            st.session_state["current_page"] = "Interrogation"
            st.rerun()
    
    with col3:
        if st.button("📋 Review Evidence", use_container_width=True):
            st.session_state["current_page"] = "Evidence"
            st.rerun()

if __name__ == "__main__":
    show_accusation_page()