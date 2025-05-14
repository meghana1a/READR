# READR: RAG Enhanced Auxiliary Domain Reader

## Overview
READR is an intelligent reading companion for classic literature that uses Retrieval-Augmented Generation (RAG) to enhance the reading experience. It provides deeper insights into literary works by retrieving relevant contextual information such as historical background, author insights, critical analyses, and thematic elements from trusted sources.

## Features
- **Smart Context Retrieval**: Automatically fetches relevant information from various knowledge sources
- **Interactive Q&A**: Ask questions about symbolism, character motivations, historical context, and more
- **Multi-Agent System**: Specialized agents work together to provide comprehensive literary analysis
- **Document Analysis**: Upload and analyze literary texts in various formats (PDF, TXT)
- **External Knowledge Integration**: Incorporates information from Wikipedia and other trusted sources
- **Interactive Visualizations**: Visual representations of character networks, themes, and symbols
- **Study Guide Generation**: Creates comprehensive study guides with summaries, character analyses, and discussion questions
- **Reading Mode**: Track reading progress and receive contextual insights while reading
- **Literary Comparisons**: Compare different literary works to identify similarities and differences

## Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation
1. Clone this repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your OpenAI API key: `OPENAI_API_KEY=your_key_here`. You can make a copy of the `.env.example` file and rename it to `.env` for this step.
6. Download SpaCy model (for entity recognition): `python -m spacy download en_core_web_sm`
7. Run the application: `python -m streamlit run app.py`

## Usage

### Basic Usage
1. Upload a literary text (PDF or TXT format)
   - You can use the provided sample text in `sample_texts/the_great_gatsby.txt`
2. Select an analysis focus from the dropdown in the sidebar:
   - General: Overall analysis
   - Historical Context: Focus on time period and historical influences
   - Character Analysis: Deep dive into character motivations and development
   - Symbolism: Analysis of symbols and their meanings
   - Themes: Exploration of major themes and motifs
   - Literary Techniques: Analysis of writing techniques and style
3. Navigate between the different tabs to access various features:
   - **Chat**: Ask questions and receive AI-powered responses
   - **Visualizations**: View interactive visual representations of the text
   - **Study Guide**: Access a comprehensive study guide for the text
   - **Reading Mode**: Read the text with contextual insights

### Advanced Features

#### Chat Interface
1. Ask questions about the text in the chat input at the bottom of the Chat tab
2. Receive comprehensive responses that combine textual evidence, historical context, and literary analysis
3. The multi-agent system provides insights from different perspectives (textual, historical, analytical)

#### Visualizations
1. Click the 'Generate Visualizations' button in the sidebar
2. View interactive visualizations including:
   - Character Network: Shows relationships between characters
   - Theme Analysis: Radar chart of major themes and their importance
   - Symbol Analysis: Bubble chart of symbols and their significance

#### Study Guide
1. Click the 'Generate Study Guide' button in the sidebar
2. Access a comprehensive study guide with sections for:
   - Summary
   - Key Characters
   - Major Themes
   - Important Symbols
   - Discussion Questions
   - Key Passages

#### Reading Mode
1. Navigate to the Reading Mode tab to read the text
2. Use the slider to track your reading position
3. Click 'Get Reading Insights' to receive contextual information about your current position in the text
4. View insights about the current scene, active characters, and questions to consider

### Example Questions

Here are some example questions you can ask about literary texts:

- "What are the main themes in this excerpt?"
- "Analyze the character of the narrator in this passage."
- "What does [symbol] symbolize in the context of this story?"
- "Explain the historical context of [time period] that relates to this text."
- "How does the author's writing style contribute to the tone of the passage?"
- "Compare the motivations of [character1] and [character2]."
- "What literary devices are used in this excerpt?"

## Architecture

### Core Components

READR is built with a sophisticated architecture that combines several advanced technologies:

1. **Vector Database**: Uses ChromaDB for efficient semantic search of document chunks
2. **Embedding System**: Utilizes OpenAI embeddings to convert text into vector representations
3. **Large Language Models**: Leverages OpenAI's GPT-4o for natural language understanding and generation
4. **Retrieval-Augmented Generation (RAG)**: Enhances responses with relevant retrieved information
5. **Multi-Agent System**: Coordinates specialized agents for comprehensive analysis

### Agent System

READR uses a multi-agent system built on LangChain and OpenAI's models, with specialized agents for different aspects of literary analysis:

- **Reader Agent**: Processes and understands the literary text, identifying key elements such as plot points, characters, settings, and narrative structure
- **Context Agent**: Retrieves historical, cultural, and biographical context relevant to the text and time period
- **Analysis Agent**: Provides literary analysis of themes, symbolism, character development, and writing techniques
- **Synthesis Agent**: Combines insights from all agents to provide comprehensive, cohesive responses

### Advanced Features

- **Visualization Engine**: Creates interactive visualizations using Plotly and NetworkX
- **Study Guide Generator**: Produces comprehensive study materials with structured sections
- **Reading Progress Tracker**: Monitors reading position and provides contextual insights
- **Conversational Chain**: Maintains context across multiple interactions

### How It Works

1. The **Document Processor** analyzes your uploaded text, breaking it into meaningful chunks and creating vector embeddings
2. The **Knowledge Retriever** fetches relevant external information from sources like Wikipedia
3. When you ask a question, all agents work in parallel to analyze different aspects of the text:
   - Reader Agent focuses on factual information from the text
   - Context Agent provides historical and biographical context
   - Analysis Agent offers literary interpretation and critical analysis
4. The Synthesis Agent combines these insights into a comprehensive response
5. For advanced features, specialized components generate visualizations, study guides, and reading insights

This multi-layered approach provides a much richer understanding of literary texts than a simple summary or analysis would offer, creating a truly intelligent reading companion.
