import streamlit as st
from agents import web_search_agent, blog_writer_agent, seo_improvement_agent

# --- Page Configuration ---
st.set_page_config(
    page_title="Multi-Agent Blog Writer",
    page_icon="✍️",
    layout="wide"
)

# --- App Title and Description ---
st.title("Multi-Agent LinkedIn Blog Post Writer ✍️")
st.markdown("""
This application leverages a multi-agent system to create SEO-optimized LinkedIn blog posts.
Enter a topic, and the agents will work together to research, write, and refine a post for you.
""")

# --- Input Section ---
st.header("1. Enter Your Blog Post Topic")
topic = st.text_input("e.g., The Future of Renewable Energy", key="topic_input")

# --- Workflow Execution ---
if st.button("Generate Blog Post", key="generate_button"):
    if topic:
        #st.spinner to show a loading message while the agents are working
        with st.spinner("Agent 1: Researching topic... Please wait."):
            research_context = web_search_agent(topic)
        
        st.success("Research complete!")

        # columns to display the workflow steps
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Step 1: Research Data")
            with st.expander("View Research"):
                st.write(research_context)

        with col2:
            with st.spinner("Agent 2: Writing first draft..."):
                draft_post = blog_writer_agent(research_context, topic)
            st.subheader("Step 2: First Draft")
            st.write(draft_post)
        
        with col3:
            with st.spinner("Agent 3: Analyzing and improving for SEO..."):
                final_post = seo_improvement_agent(draft_post, topic)
            st.subheader("Step 3: Final SEO-Optimized Post")
            st.write(final_post)

        st.header("🎉 Your Blog Post is Ready! 🎉")

    else:
        st.error("Please enter a topic to generate a blog post.")