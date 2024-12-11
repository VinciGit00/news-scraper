import streamlit as st
from scrapegraph_py import Client
from scrapegraph_py.logger import sgai_logger

websites = {
    "cnn": "https://edition.cnn.com",
    "bbc": "https://www.bbc.com",
    "ny_times":"https://www.nytimes.com",
    "reuters": "https://www.reuters.com",
    "associated_press": "https://apnews.com"
}

def scrape_news(api_key, website_url):
    try:
        sgai_logger.set_logging(level="INFO")
        sgai_client = Client(api_key=api_key)
        
        response = sgai_client.smartscraper(
            website_url=website_url,
            user_prompt="Extract me all the news",
        )
        
        sgai_client.close()
        return response['result']
    except Exception as e:
        return f"Error occurred: {str(e)}"

def summarize_news(api_key, website_url):
    try:
        sgai_logger.set_logging(level="INFO")
        sgai_client = Client(api_key=api_key)
        
        response = sgai_client.smartscraper(
            website_url=website_url,
            user_prompt="Extract the main heading, description, and summary of the webpage",
        )
        
        sgai_client.close()
        return response['result']
    except Exception as e:
        return f"Error occurred: {str(e)}"

def main():
    st.title("🌍 News Website Scraper")
    
    # API Key input
    api_key = st.text_input("Enter your ScrapeGraph API Key:", type="password")

    st.write("### Refill ScrapeGraph's API Keys at [https://scrapegraphai.com](https://scrapegraphai.com)")

    # Create dropdown menu
    selected_website = st.selectbox(
        "Choose a news website:",
        options=list(websites.keys()),
        format_func=lambda x: x.replace('_', ' ').title()
    )
    
    # Create two columns for just the buttons
    col1, col2 = st.columns(2)
    
    scrape_clicked = col1.button("Extract News")
    summary_clicked = col2.button("Make Summary")
    
    # Results section using full width
    if scrape_clicked or summary_clicked:
        if not api_key:
            st.error("Please enter your API key first!")
        else:
            if scrape_clicked:
                with st.spinner('Scraping news...'):
                    news_data = scrape_news(api_key, websites[selected_website])
                    st.write("### Scraped News")
                    st.write(news_data)
            
            if summary_clicked:
                with st.spinner('Creating summary...'):
                    summary_data = summarize_news(api_key, websites[selected_website])
                    st.write("### News Summary")
                    st.write(summary_data)

if __name__ == "__main__":
    main()