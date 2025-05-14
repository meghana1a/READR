import os
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
import streamlit as st
import json
from typing import Dict, List, Any, Optional

class StreamHandler(BaseCallbackHandler):
    """Callback handler for streaming LLM responses to a Streamlit app."""
    
    def __init__(self, container):
        self.container = container
        self.text = ""
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Run on new LLM token."""
        self.text += token
        self.container.markdown(self.text)

class AdvancedFeatures:
    """Implements advanced features for the READR application."""
    
    def __init__(self):
        """Initialize advanced features."""
        # Initialize LLM with minimal parameters to avoid compatibility issues
        self.llm = ChatOpenAI(temperature=0.7)
    
    def create_conversational_chain(self, vectorstore):
        """Create a conversational retrieval chain for more natural interactions.
        
        Args:
            vectorstore: Vector store containing document chunks
            
        Returns:
            ConversationalRetrievalChain: Chain for conversational retrieval
        """
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Create custom prompt for literary analysis
        prompt_template = """
        You are a literary scholar and expert on classic literature. Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        
        Context:
        {context}
        
        Chat History:
        {chat_history}
        
        Question: {question}
        
        Answer:
        """
        
        PROMPT = PromptTemplate(
            template=prompt_template, 
            input_variables=["context", "chat_history", "question"]
        )
        
        chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=vectorstore.as_retriever(),
            memory=memory,
            combine_docs_chain_kwargs={"prompt": PROMPT}
        )
        
        return chain
    
    def generate_literary_visualizations(self, text, analysis_type):
        """Generate visualization data for literary analysis.
        
        Args:
            text: Text to analyze
            analysis_type: Type of analysis
            
        Returns:
            dict: Visualization data
        """
        # Prepare prompt based on analysis type
        if analysis_type == "Character Analysis":
            prompt = f"""Analyze the characters in the following text and generate a JSON object with:
            1. Character names as keys
            2. For each character, include: traits, relationships, development, importance (1-10)
            Text: {text}
            Output only valid JSON without explanation."""
        
        elif analysis_type == "Themes":
            prompt = f"""Identify the main themes in the following text and generate a JSON object with:
            1. Theme names as keys
            2. For each theme, include: description, evidence, importance (1-10)
            Text: {text}
            Output only valid JSON without explanation."""
        
        elif analysis_type == "Symbolism":
            prompt = f"""Identify symbols in the following text and generate a JSON object with:
            1. Symbol names as keys
            2. For each symbol, include: meaning, occurrences, significance (1-10)
            Text: {text}
            Output only valid JSON without explanation."""
        
        else:  # General analysis
            prompt = f"""Perform a general literary analysis of the following text and generate a JSON object with:
            1. Key elements: characters, themes, symbols, setting
            2. For each element, include relevant details and importance (1-10)
            Text: {text}
            Output only valid JSON without explanation."""
        
        # Generate analysis
        response = self.llm.invoke(prompt)
        
        # Parse JSON response
        try:
            # Extract JSON from response if needed
            response_text = response.content
            # Find JSON in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}')
            if json_start != -1 and json_end != -1:
                json_str = response_text[json_start:json_end+1]
                visualization_data = json.loads(json_str)
            else:
                visualization_data = json.loads(response_text)
            return visualization_data
        except Exception as e:
            st.error(f"Error parsing visualization data: {str(e)}")
            return {}
    
    def compare_literary_works(self, text1, text2):
        """Compare two literary texts and identify similarities and differences.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            dict: Comparison results
        """
        prompt = f"""Compare the following two literary texts and identify similarities and differences in:
        1. Themes
        2. Style
        3. Characters
        4. Setting
        5. Tone
        
        Text 1: {text1[:1000]}...
        
        Text 2: {text2[:1000]}...
        
        Generate a JSON object with these categories and detailed comparisons.
        Output only valid JSON without explanation."""
        
        # Generate comparison
        response = self.llm.invoke(prompt)
        
        # Parse JSON response
        try:
            # Extract JSON from response
            response_text = response.content
            # Find JSON in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}')
            if json_start != -1 and json_end != -1:
                json_str = response_text[json_start:json_end+1]
                comparison_data = json.loads(json_str)
            else:
                comparison_data = json.loads(response_text)
            return comparison_data
        except Exception as e:
            st.error(f"Error parsing comparison data: {str(e)}")
            return {}
    
    def generate_study_guide(self, text, title=None, author=None):
        """Generate a comprehensive study guide for a literary text.
        
        Args:
            text: Literary text
            title: Title of the work
            author: Author of the work
            
        Returns:
            dict: Study guide content
        """
        # Prepare context
        context = f"Title: {title}\nAuthor: {author}\n" if title and author else ""
        
        prompt = f"""Generate a comprehensive study guide for the following literary text:
        
        {context}Text: {text[:2000]}...
        
        Include the following sections in JSON format:
        1. Summary
        2. Key Characters (name, description, significance)
        3. Major Themes (name, explanation, textual evidence)
        4. Important Symbols (symbol, meaning, occurrences)
        5. Discussion Questions (at least 5 thought-provoking questions)
        6. Key Passages (passage text, page/location, significance)
        7. Historical Context (relevant historical information)
        8. Critical Perspectives (different ways to interpret the text)
        
        Output only valid JSON without explanation."""
        
        # Generate study guide
        response = self.llm.invoke(prompt)
        
        # Parse JSON response
        try:
            # Extract JSON from response
            response_text = response.content
            # Find JSON in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}')
            if json_start != -1 and json_end != -1:
                json_str = response_text[json_start:json_end+1]
                study_guide = json.loads(json_str)
            else:
                study_guide = json.loads(response_text)
            return study_guide
        except Exception as e:
            st.error(f"Error parsing study guide data: {str(e)}")
            return {}
    
    def track_reading_progress(self, text, current_position):
        """Track reading progress and provide contextual insights.
        
        Args:
            text: Full text
            current_position: Current reading position
            
        Returns:
            dict: Progress data and contextual insights
        """
        # Calculate progress percentage
        total_length = len(text)
        progress_percentage = (current_position / total_length) * 100 if total_length > 0 else 0
        
        # Get current context (text around current position)
        start_pos = max(0, current_position - 500)
        end_pos = min(total_length, current_position + 500)
        current_context = text[start_pos:end_pos]
        
        # Generate contextual insights
        prompt = f"""The reader is currently at this point in the text:
        
        {current_context}
        
        Generate contextual insights in JSON format including:
        1. Current scene summary
        2. Active characters
        3. Important elements to pay attention to
        4. Questions to consider while reading this section
        
        Output only valid JSON without explanation."""
        
        # Generate insights
        response = self.llm.invoke(prompt)
        
        # Parse JSON response
        try:
            # Extract JSON from response
            response_text = response.content
            # Find JSON in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}')
            if json_start != -1 and json_end != -1:
                json_str = response_text[json_start:json_end+1]
                insights = json.loads(json_str)
            else:
                insights = json.loads(response_text)
                
            # Combine progress data with insights
            progress_data = {
                "progress_percentage": progress_percentage,
                "current_position": current_position,
                "total_length": total_length,
                "insights": insights
            }
            
            return progress_data
        except Exception as e:
            st.error(f"Error parsing progress data: {str(e)}")
            return {
                "progress_percentage": progress_percentage,
                "current_position": current_position,
                "total_length": total_length,
                "insights": {}
            }
