import streamlit as st
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Import components
from components.document_processor import DocumentProcessor
from components.agent_system import AgentSystem
from components.knowledge_retriever import KnowledgeRetriever
from components.ui_components import setup_ui, display_response
from components.advanced_features import AdvancedFeatures
from components.visualizations import LiteraryVisualizations

# Set page configuration
st.set_page_config(page_title="READR: Literary Companion", layout="wide")

# Setup UI components
setup_ui()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Welcome to READR! Please upload a literary text to begin exploring."}]

if "document_processor" not in st.session_state:
    st.session_state["document_processor"] = DocumentProcessor()

if "knowledge_retriever" not in st.session_state:
    st.session_state["knowledge_retriever"] = KnowledgeRetriever()

if "agent_system" not in st.session_state:
    st.session_state["agent_system"] = AgentSystem()
    
if "advanced_features" not in st.session_state:
    st.session_state["advanced_features"] = AdvancedFeatures()
    
if "visualizations" not in st.session_state:
    st.session_state["visualizations"] = LiteraryVisualizations()
    
if "current_tab" not in st.session_state:
    st.session_state["current_tab"] = "Chat"
    
if "study_guide" not in st.session_state:
    st.session_state["study_guide"] = None
    
if "visualization_data" not in st.session_state:
    st.session_state["visualization_data"] = None
    
if "reading_position" not in st.session_state:
    st.session_state["reading_position"] = 0

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["Chat", "Visualizations", "Study Guide", "Reading Mode"])

# File uploader in sidebar
with st.sidebar:
    st.header("Upload Literary Text")
    uploaded_files = st.file_uploader(
        "Choose a file", 
        type=["txt", "pdf"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        # Process uploaded documents
        document_processor = st.session_state["document_processor"]
        knowledge_base = document_processor.process_documents(uploaded_files)
        st.session_state["knowledge_base"] = knowledge_base
        
        # Extract combined text for visualizations and study guide
        combined_text = ""
        for uploaded_file in uploaded_files:
            if uploaded_file.type == "application/pdf":
                file_content = document_processor.extract_pdf_text(uploaded_file)
            else:  # Assume text file
                file_content = uploaded_file.read().decode("utf-8")
            combined_text += file_content + "\n\n"
        
        st.session_state["combined_text"] = combined_text
        
        # Display document information
        st.success(f"Processed {len(uploaded_files)} document(s)")
        
        # Analysis options
        st.header("Analysis Options")
        analysis_type = st.selectbox(
            "Select analysis focus:",
            ["General", "Historical Context", "Character Analysis", "Symbolism", "Themes", "Literary Techniques"]
        )
        st.session_state["analysis_type"] = analysis_type
        
        # Advanced options
        st.header("Advanced Features")
        if st.button("Generate Study Guide"):
            with st.spinner("Generating comprehensive study guide..."):
                advanced_features = st.session_state["advanced_features"]
                study_guide = advanced_features.generate_study_guide(combined_text)
                st.session_state["study_guide"] = study_guide
                st.session_state["current_tab"] = "Study Guide"
                st.rerun()
        
        if st.button("Generate Visualizations"):
            with st.spinner("Analyzing text and generating visualizations..."):
                advanced_features = st.session_state["advanced_features"]
                visualization_data = advanced_features.generate_literary_visualizations(combined_text, analysis_type)
                st.session_state["visualization_data"] = visualization_data
                st.session_state["current_tab"] = "Visualizations"
                st.rerun()

# Tab 1: Chat Interface
with tab1:
    # Display chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    # Chat input
    question = st.chat_input(
        "Ask about the literary text...",
        disabled=not uploaded_files,
    )
    
    # Process question
    if question and uploaded_files:
        # Add user question to chat history
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("user").write(question)
        
        # Get response from agent system
        agent_system = st.session_state["agent_system"]
        knowledge_retriever = st.session_state["knowledge_retriever"]
        knowledge_base = st.session_state["knowledge_base"]
        analysis_type = st.session_state.get("analysis_type", "General")
        
        # Display streaming response
        with st.chat_message("assistant"):
            response_container = st.empty()
            
            # Generate response
            response = agent_system.generate_response(
                question=question,
                knowledge_base=knowledge_base,
                knowledge_retriever=knowledge_retriever,
                analysis_type=analysis_type,
                chat_history=st.session_state.messages,
                response_container=response_container
            )
            
            # Add response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

# Tab 2: Visualizations
with tab2:
    st.header("Literary Analysis Visualizations")
    
    if not uploaded_files:
        st.info("Please upload a literary text to generate visualizations.")
    elif st.session_state["visualization_data"] is None:
        st.info("Click 'Generate Visualizations' in the sidebar to analyze the text.")
    else:
        visualization_data = st.session_state["visualization_data"]
        visualizations = st.session_state["visualizations"]
        
        # Determine what kind of visualization data we have
        if "characters" in visualization_data:
            st.subheader("Character Network")
            try:
                character_fig = visualizations.character_network(visualization_data["characters"])
                st.plotly_chart(character_fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error generating character network: {str(e)}")
        
        if "themes" in visualization_data:
            st.subheader("Theme Analysis")
            try:
                theme_fig = visualizations.theme_radar_chart(visualization_data["themes"])
                st.plotly_chart(theme_fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error generating theme analysis: {str(e)}")
        
        if "symbols" in visualization_data:
            st.subheader("Symbol Analysis")
            try:
                symbol_fig = visualizations.symbol_bubble_chart(visualization_data["symbols"])
                st.plotly_chart(symbol_fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error generating symbol analysis: {str(e)}")

# Tab 3: Study Guide
with tab3:
    if not uploaded_files:
        st.info("Please upload a literary text to generate a study guide.")
    elif st.session_state["study_guide"] is None:
        st.info("Click 'Generate Study Guide' in the sidebar to create a comprehensive study guide.")
    else:
        study_guide_data = st.session_state["study_guide"]
        visualizations = st.session_state["visualizations"]
        visualizations.create_study_guide_ui(study_guide_data)

# Tab 4: Reading Mode
with tab4:
    st.header("Reading Mode")
    
    if not uploaded_files:
        st.info("Please upload a literary text to use Reading Mode.")
    else:
        combined_text = st.session_state["combined_text"]
        
        # Display text with progress tracking
        st.subheader("Text")
        text_container = st.container()
        with text_container:
            st.markdown(combined_text[:5000] + "..." if len(combined_text) > 5000 else combined_text)
        
        # Track reading progress
        reading_position = st.slider("Reading Position", 0, len(combined_text), st.session_state["reading_position"])
        st.session_state["reading_position"] = reading_position
        
        # Generate reading insights
        if st.button("Get Reading Insights"):
            with st.spinner("Analyzing your current reading position..."):
                advanced_features = st.session_state["advanced_features"]
                progress_data = advanced_features.track_reading_progress(combined_text, reading_position)
                visualizations = st.session_state["visualizations"]
                visualizations.display_reading_progress(progress_data)
