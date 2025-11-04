# import the necessary libraries
import os
from dotenv import load_dotenv
from tavily import TavilyClient

# Import the Hugging Face pipeline
from transformers import pipeline
import torch

# Load the environment variables from the .env file
load_dotenv()

# --- AGENT 1: WEB SEARCH AGENT ---

# Get the Tavily API key from the environment variables
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in .env file. Please add it.")

# Initialize the Tavily client
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

def web_search_agent(topic: str) -> str:
    """
    This function takes a topic string and uses the Tavily API to search the web.
    """
    print(f"--- Starting Web Search for: {topic} ---")
    try:
        response = tavily_client.search(
            query=topic, 
            search_depth="basic",
            max_results=5
        )
        results = response['results']
        
        formatted_results = ""
        for i, res in enumerate(results):
            formatted_results += f"Result {i+1}:\n"
            formatted_results += f"Title: {res['title']}\n"
            formatted_results += f"URL: {res['url']}\n"
            formatted_results += f"Content: {res['content']}\n\n"
        
        print("--- Web Search Finished ---")
        return formatted_results
    except Exception as e:
        print(f"An error occurred during web search: {e}")
        return f"Error: Could not perform web search for {topic}."

# --- AGENT 2: BLOG WRITER AGENT ---

# initialize one pipeline and can reuse it for both writing agents
print("--- Initializing LLM Agent with Qwen/Qwen2-0.5B-Instruct ---")
llm_agent = pipeline(
    "text-generation",
    model="Qwen/Qwen2-0.5B-Instruct",
    device="cpu",
)
print("--- LLM Agent Initialized ---")

def blog_writer_agent(search_results: str, topic: str) -> str:
    """
    This function takes search results and a topic, then generates a blog post draft.
    """
    print("--- Starting Blog Post Generation ---")
    try:
        prompt = f"""
        You are a professional content creator specializing in technology blog posts for LinkedIn.
        Your task is to write an engaging and informative blog post on the topic: "{topic}".
        You have been provided with the following research material:
        --- RESEARCH ---
        {search_results}
        --- END OF RESEARCH ---
        Please write a well-structured blog post based *only* on the provided research.
        The post should have a catchy title, a brief introduction, a main body with key points, a conclusion, and relevant hashtags.
        """
        response = llm_agent(prompt, max_new_tokens=1024)
        generated_post = response[0]['generated_text']
        clean_post = generated_post.split(prompt)[-1].strip()
        print("--- Blog Post Generation Finished ---")
        return clean_post
    except Exception as e:
        print(f"An error occurred during blog generation: {e}")
        return f"Error: Could not generate blog post for {topic}."

# --- AGENT 3: SEO IMPROVEMENT AGENT ---

def seo_improvement_agent(blog_post: str, topic: str) -> str:
    """
    This function takes a blog post and improves it for SEO.
    """
    print("--- Starting SEO Analysis and Improvement ---")
    try:
        # This prompt is highly specific to the SEO task
        prompt = f"""
        You are an expert SEO analyst. Your task is to improve the following LinkedIn blog post draft for better search engine visibility.
        The primary keyword for the post is "{topic}".

        --- BLOG POST DRAFT ---
        {blog_post}
        --- END OF DRAFT ---

        Please perform the following actions:
        1. Create a new, compelling title for the blog post. The title must be under 60 characters and contain the primary keyword.
        2. Write a meta description for the post. The description must be under 160 characters, be engaging, and contain the primary keyword.
        3. Review the entire blog post. Ensure the primary keyword appears naturally in the introduction and at least once in the main body.
        4. Rewrite the entire blog post, incorporating all of the above improvements.

        Your final output should be the improved blog post, starting with the new title, followed by the meta description, and then the full rewritten article with hashtags.
        Format it like this:
        New Title: [Your new title here]
        Meta Description: [Your meta description here]
        ---
        [Full rewritten blog post text here]
        """
        response = llm_agent(prompt, max_new_tokens=1024)
        generated_post = response[0]['generated_text']
        clean_post = generated_post.split(prompt)[-1].strip()
        print("--- SEO Improvement Finished ---")
        return clean_post
    except Exception as e:
        print(f"An error occurred during SEO improvement: {e}")
        return f"Error: Could not improve blog post."


# --- Main execution block to test the full workflow ---
if __name__ == "__main__":
    blog_topic = "The Rise of Multi-Agent AI Systems in 2025"

    # --- Step 1: Run the Web Search Agent ---
    research_context = web_search_agent(blog_topic)
    
    if "Error:" not in research_context:
        # --- Step 2: Run the Blog Writer Agent ---
        draft_post = blog_writer_agent(search_results=research_context, topic=blog_topic)

        if "Error:" not in draft_post:
            # --- Step 3: Run the SEO Improvement Agent ---
            final_post = seo_improvement_agent(blog_post=draft_post, topic=blog_topic)

            # --- Step 4: Print the final, optimized output ---
            print("\n\n--- FINAL SEO-OPTIMIZED BLOG POST ---")
            print(final_post)