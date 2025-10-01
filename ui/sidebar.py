import streamlit as st


def navigate():
    # Initialize session state if not exists
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Home"
    if "game_started" not in st.session_state:
        st.session_state["game_started"] = False
    
    with st.sidebar:
        # OpenAI API Key section
        st.markdown("### 🔑 OpenAI API Key")
        api_key_input = st.text_input(
            "Enter your OpenAI API Key:",
            value=st.session_state.get("openai_api_key", ""),
            type="password",
            help="Get your API key from https://platform.openai.com/api-keys",
            key="api_key_input"
        )
        
        # Save API key to session state
        if api_key_input:
            st.session_state["openai_api_key"] = api_key_input
        
        # Show API key status
        if st.session_state.get("openai_api_key"):
            st.success("✅ API Key Set")
        else:
            st.warning("⚠️ API Key Required")
        
        st.markdown("---")
        
        # Show different navigation options based on game state
        if st.session_state["game_started"]:
            page = st.radio(
                "Navigate the game:",
                ("Briefing", "Interrogation", "Evidence", "Accusation", "Hints"),
                index=["Briefing", "Interrogation", "Evidence", "Accusation", "Hints"].index(st.session_state["current_page"]) if st.session_state["current_page"] != "Home" else 0
            )
            st.session_state["current_page"] = page
        else:
            page = st.radio(
                "Navigate the game:",
                ("Home",),
                index=0
            )
            st.session_state["current_page"] = page
            
        # Show game info if game has started
        if st.session_state["game_started"] and "selected_theme" in st.session_state:
            st.markdown("---")
            st.markdown(f"**Theme:** {st.session_state['selected_theme']}")
            
        # Reset game button
        if st.session_state["game_started"]:
            st.markdown("---")
            if st.button("🔄 Reset Game", use_container_width=True):
                # Clear game state
                for key in ["game_started", "selected_theme", "current_page", "mystery_case", "game_engine"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
    
    return st.session_state["current_page"]