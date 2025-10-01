from ui.home import show_home_page
from ui.accusation import show_accusation_page
from ui.evidence import show_evidence_page
from ui.briefing import show_briefing_page
from ui.interrogation import show_interrogation_page
from ui.sidebar import navigate
from ui.hints import show_hints_page
import streamlit as st

page = navigate()
if page == "Home":
     show_home_page()
elif page == "Accusation":
     show_accusation_page()
elif page == "Evidence":
     show_evidence_page()
elif page == "Briefing":
     show_briefing_page()
elif page == "Hints":
     show_hints_page()
elif page == 'Interrogation':
     show_interrogation_page()     