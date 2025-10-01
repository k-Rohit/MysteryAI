"""
AI-Powered Mystery Solving Game Engine
Uses LangChain and OpenAI to generate mysteries and provide interactive gameplay
"""

import os
import json
from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# Data Models
class Suspect(BaseModel):
    """Model for a suspect in the mystery"""
    name: str = Field(description="Name of the suspect")
    age: int = Field(description="Age of the suspect")
    occupation: str = Field(description="Their job or role")
    alibi: str = Field(description="Their claimed whereabouts during the crime")
    motive: str = Field(description="Potential reason they might have committed the crime")
    personality: str = Field(description="Brief personality description")
    secret: str = Field(description="A secret they're hiding (may or may not be related to crime)")


class Evidence(BaseModel):
    """Model for a piece of evidence"""
    name: str = Field(description="Name/type of evidence")
    description: str = Field(description="Detailed description of the evidence")
    location: str = Field(description="Where it was found")
    significance: str = Field(description="Why this evidence matters")


class MysteryCase(BaseModel):
    """Complete mystery case structure"""
    title: str = Field(description="Engaging title for the mystery")
    setting: str = Field(description="Location and time period")
    victim: str = Field(description="Name and brief description of victim")
    crime: str = Field(description="What crime was committed")
    initial_scene: str = Field(description="Description of what player sees when they arrive")
    suspects: List[Suspect] = Field(description="List of 3-5 suspects")
    evidence: List[Evidence] = Field(description="List of 4-6 pieces of evidence")
    solution: str = Field(description="Who did it and how (hidden from player)")
    key_clues: List[str] = Field(description="Critical clues that point to the solution")


class MysteryGameEngine:
    """Main game engine for generating and managing mysteries"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(
            temperature=0.8,
            model=model,
            openai_api_key=api_key
        )
        self.case: Optional[MysteryCase] = None
        self.discovered_clues: List[str] = []
        self.interrogation_history: Dict[str, List[str]] = {}
        
    def generate_mystery(self, theme: str = "classic detective") -> MysteryCase:
        """Generate a complete mystery case"""
        parser = PydanticOutputParser(pydantic_object=MysteryCase)
        
        prompt = ChatPromptTemplate.from_template(
            """You are a master mystery writer specializing in Indian settings. Create a compelling, solvable mystery case with rich, atmospheric details set in India.
            
            Theme: {theme}
            
            Requirements:
            - The mystery must be logically solvable with the given clues
            - Include red herrings but make sure the real solution is deducible
            - Make suspects interesting with complex motivations and detailed backgrounds
            - Evidence should connect in meaningful ways
            - The solution should be surprising but fair
            - Include authentic Indian cultural elements, names, locations, and context
            - Use Indian names for characters (mix of Hindi, regional, and modern Indian names)
            - Include Indian cultural references, food, festivals, traditions where relevant
            
            Writing Style Requirements:
            - Write in a noir/mystery style with atmospheric descriptions of Indian settings
            - Make the initial_scene vivid and immersive (200-300 words) with Indian cultural context
            - Give detailed, believable alibis for each suspect (50-100 words each) with Indian locations and customs
            - Include specific details about times, locations, and circumstances in Indian context
            - Use descriptive language that captures Indian atmosphere and culture
            - Make victim descriptions rich with personality and Indian background
            - Ensure evidence has compelling descriptions and clear significance
            - Include references to Indian cities, landmarks, cultural practices, and social dynamics
            
            {format_instructions}
            
            Create a complete mystery case now:"""
        )
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "theme": theme,
            "format_instructions": parser.get_format_instructions()
        })
        
        self.case = parser.parse(response.content)
        return self.case
    
    def get_initial_briefing(self) -> str:
        """Get the initial case briefing for the player"""
        if not self.case:
            return "No case loaded. Generate a mystery first."
        
        briefing = f"""
╔════════════════════════════════════════════════════════════╗
║  {self.case.title.upper().center(56)}  ║
╚════════════════════════════════════════════════════════════╝

SETTING: {self.case.setting}

VICTIM: {self.case.victim}

CRIME: {self.case.crime}

═══════════════════════════════════════════════════════════

THE SCENE:
{self.case.initial_scene}

═══════════════════════════════════════════════════════════

SUSPECTS:
"""
        for i, suspect in enumerate(self.case.suspects, 1):
            briefing += f"\n{i}. {suspect.name} - {suspect.occupation}, Age {suspect.age}"
        
        briefing += "\n\n═══════════════════════════════════════════════════════════\n"
        briefing += "\nYour investigation begins now, Detective.\n"
        
        return briefing
    
    def interrogate_suspect(self, suspect_name: str, question: str) -> str:
        """Interrogate a suspect with a specific question"""
        if not self.case:
            return "No active case."
        
        # Find the suspect
        suspect = next((s for s in self.case.suspects if s.name.lower() == suspect_name.lower()), None)
        if not suspect:
            return f"Suspect '{suspect_name}' not found."
        
        # Track interrogation history
        if suspect_name not in self.interrogation_history:
            self.interrogation_history[suspect_name] = []
        self.interrogation_history[suspect_name].append(question)
        
        # Generate response using AI
        prompt = ChatPromptTemplate.from_template(
            """You are playing {name}, a suspect in a murder mystery.
            
            Your character details:
            - Occupation: {occupation}
            - Age: {age}
            - Personality: {personality}
            - Alibi: {alibi}
            - Motive: {motive}
            - Secret: {secret}
            
            The crime: {crime}
            
            Previous questions you've been asked: {history}
            
            The detective asks: "{question}"
            
            Respond in character. Be somewhat evasive about your secret, but provide useful information.
            If the question is about something you wouldn't know, say so. Stay consistent with your alibi
            and character details. Show some personality and emotion.
            
            Your response (150 words max):"""
        )
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "name": suspect.name,
            "occupation": suspect.occupation,
            "age": suspect.age,
            "personality": suspect.personality,
            "alibi": suspect.alibi,
            "motive": suspect.motive,
            "secret": suspect.secret,
            "crime": self.case.crime,
            "history": "\n".join(self.interrogation_history[suspect_name][:-1]) or "None",
            "question": question
        })
        
        return f"\n{suspect.name}: \"{response.content}\"\n"
    
    def examine_evidence(self, evidence_name: str) -> str:
        """Get detailed analysis of evidence"""
        if not self.case:
            return "No active case."
        
        evidence = next((e for e in self.case.evidence if e.name.lower() in evidence_name.lower()), None)
        if not evidence:
            return f"Evidence '{evidence_name}' not found."
        
        # Generate deeper analysis
        prompt = ChatPromptTemplate.from_template(
            """As a forensic expert, provide a detailed analysis of this evidence:
            
            Evidence: {name}
            Description: {description}
            Found at: {location}
            
            Context: This is part of a case involving: {crime}
            
            Provide additional forensic insights, possible interpretations, and what questions
            this evidence raises. Keep it under 200 words and make it feel like a professional
            forensic report.
            
            Analysis:"""
        )
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "name": evidence.name,
            "description": evidence.description,
            "location": evidence.location,
            "crime": self.case.crime
        })
        
        analysis = f"""
╔════════════════════════════════════════════════════════════╗
║  EVIDENCE ANALYSIS: {evidence.name.upper().center(37)}  ║
╚════════════════════════════════════════════════════════════╝

DESCRIPTION: {evidence.description}

LOCATION: {evidence.location}

SIGNIFICANCE: {evidence.significance}

FORENSIC ANALYSIS:
{response.content}
"""
        return analysis
    
    def get_hint(self, difficulty: str = "medium") -> str:
        """Generate a contextual hint based on investigation progress"""
        if not self.case:
            return "No active case."
        
        prompt = ChatPromptTemplate.from_template(
            """You are helping a detective solve a mystery. Based on their investigation so far,
            provide a helpful hint.
            
            The solution: {solution}
            Key clues: {key_clues}
            
            Questions they've asked: {interrogations}
            
            Difficulty level: {difficulty}
            - easy: Point them directly toward the solution
            - medium: Suggest a line of inquiry or connection to explore
            - hard: Just a gentle nudge in the right direction
            
            Provide a single, helpful hint (2-3 sentences max):"""
        )
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "solution": self.case.solution,
            "key_clues": ", ".join(self.case.key_clues),
            "interrogations": str(self.interrogation_history) if self.interrogation_history else "None yet",
            "difficulty": difficulty
        })
        
        return f"\n💡 HINT: {response.content}\n"
    
    def submit_solution(self, accused: str, explanation: str) -> Dict[str, any]:
        """Submit and evaluate the player's solution"""
        if not self.case:
            return {"success": False, "message": "No active case."}
        
        prompt = ChatPromptTemplate.from_template(
            """You are evaluating a detective's solution to a mystery.
            
            The correct solution: {solution}
            Key clues that point to solution: {key_clues}
            
            Detective's accusation: {accused}
            Detective's explanation: {explanation}
            
            Evaluate if they:
            1. Identified the correct perpetrator
            2. Understood the key evidence
            3. Provided a logical explanation
            
            Respond with a JSON object:
            {{
                "correct": true/false,
                "score": 0-100,
                "feedback": "detailed feedback on their reasoning",
                "missed_clues": ["list", "of", "important", "clues", "they", "missed"]
            }}
            
            Be encouraging even if wrong. If correct, congratulate them!
            """
        )
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "solution": self.case.solution,
            "key_clues": ", ".join(self.case.key_clues),
            "accused": accused,
            "explanation": explanation
        })
        
        try:
            result = json.loads(response.content)
            return result
        except:
            # Fallback if JSON parsing fails
            return {
                "correct": accused.lower() in self.case.solution.lower(),
                "score": 50,
                "feedback": response.content,
                "missed_clues": []
            }
    
    def list_suspects(self) -> str:
        """List all suspects with brief details"""
        if not self.case:
            return "No active case."
        
        output = "\n═══ SUSPECTS ═══\n"
        for i, suspect in enumerate(self.case.suspects, 1):
            output += f"\n{i}. {suspect.name}"
            output += f"\n   {suspect.occupation}, Age {suspect.age}"
            output += f"\n   Alibi: {suspect.alibi}\n"
        return output
    
    def list_evidence(self) -> str:
        """List all available evidence"""
        if not self.case:
            return "No active case."
        
        output = "\n═══ EVIDENCE ═══\n"
        for i, evidence in enumerate(self.case.evidence, 1):
            output += f"\n{i}. {evidence.name}"
            output += f"\n   Location: {evidence.location}"
            output += f"\n   {evidence.description[:100]}...\n"
        return output


# Global game engine instance
_game_engine = None

def get_game_engine():
    """Get or create the global game engine instance"""
    global _game_engine
    
    # Try to get API key from session state first, then from environment
    try:
        import streamlit as st
        api_key = st.session_state.get("openai_api_key")
    except:
        api_key = None
    
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OpenAI API Key not found. Please enter your API key in the sidebar.")
    
    # Create new engine if API key changed or engine doesn't exist
    if _game_engine is None or (hasattr(_game_engine, '_api_key') and _game_engine._api_key != api_key):
        _game_engine = MysteryGameEngine(api_key=api_key)
        _game_engine._api_key = api_key  # Store the API key for comparison
    
    return _game_engine
