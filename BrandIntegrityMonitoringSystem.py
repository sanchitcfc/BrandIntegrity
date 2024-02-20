import openai
import streamlit as st
from PIL import Image
import pytesseract
import io
import pandas as pd


df = pd.read_csv('sample_tweets.csv')  # assuming your file is named 'sample_tweets.csv'
current_tweet_index = [0]  # use a list to make it mutable

def load_tweet(index):
    return df.iloc[index]['tweet_text'] if df.shape[0] > index else ""



def main():
    openai.api_type = "azure"
    openai.api_base = "https://cloudcafe42.openai.azure.com/"
    openai.api_version = "2023-07-01-preview"   
    openai.api_key = st.secrets["openai_api_key"]
    
    st.set_page_config(page_title="Brand Integrity Monitoring System", page_icon=":guardsman:", layout="wide")

    # Function to convert image to text
    def image_to_text(image_data):
        # Specify the path to the Tesseract executable
        pytesseract.pytesseract.tesseract_cmd = r'tesseract.exe'
        # Convert the file uploader data to bytes and then to an image
        image = Image.open(io.BytesIO(image_data.read()))
        # Use pytesseract to extract text from the image
        return pytesseract.image_to_string(image)

    def generate_openai_response(user_input, image_data):
        prompt ="Role: As the 'Brand Integrity Monitoring System', your primary function is to analyze social media content, specifically tweets, related to the airline, hotel, cruise, and transportation sectors. Your analysis is focused on identifying potential fraud. Goals:Detect Fraud:Scrutinize tweets for signs of fraudulent activity. Look for red flags such as misleading information, suspicious offers, or unrealistic promises related to these sectors.Safety Analysis: Evaluate links and phone numbers within tweets to ascertain the security and legitimacy of the websites they lead to, determining potential online threats. Response Categorization: Your responses should categorize the analysis into two main verdicts: Fraud Alert: With three subcategories: v1: Indicative of potential fraud. v2: High likelihood of fraud. v3: Certainty of fraud. Looks Safe: With three subcategories: v1: Minimal risk detected. v2: Appears significantly safe. v3: Confirmed utmost safety. Concise and Expert Communication: Maintain a casual yet expert tone. Offer direct and informed conclusions. Instructions: Analyze the content of tweets and accompanying links with a focus on detecting fraudulent activities. Provide a clear verdict (Fraud Alert or Looks Safe) with an appropriate level of certainty (v1, v2, v3). Maintain a balance between concise responses and providing necessary detail for your analysis. Stay updated with current trends and tactics in fraud related to the specified sectors. Detailed Instructions: Analyze the phone numbers provided in the tweets and try to match it with official phone numbers. Analyze Keywords in Content: Look for common fraud indicators in text, such as 'Discount', 'Offers', 'Hurry', 'Claim', 'Job opportunities'. Utilize Google Dorks and API calls for in-depth analysis.Public Review Websites Analysis: Web scrape top review websites to gather public opinions and reviews that might indicate fraudulent practices.Social Media Scrutiny: Examine social media accounts, including posts and followers, through API calls to detect any signs of fraud or scam reports.Comparison of Discounts: Identify unusual discounts by comparing prices with original websites. URL Analysis: Check URLs for similarities to well-known brands or websites, which might indicate phishing attempts.Image Processing and Recognition: Use image processing and recognition technology to detect potential fraud content in images.Domain/Account Age Verification: Use tools like the Wayback Machine to check the age of domains/accounts, as newer ones might be more suspicious.Contact Information Verification: Verify the authenticity of the contact information provided. Policy Checks: Review the website’s privacy policy and terms of service for any irregularities. Digital Certificates Inspection: Check for digital certificates such as SSL, DMARC, SPF, PKI to ensure website security.Advertisement and Pop-up Analysis: Evaluate the number and quality of advertisements and pop-ups as excessive or malicious advertising might indicate a compromised or fraudulent site."
        messages = [
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': user_input},
        ]

        if image_data:
            image_text = image_to_text(image_data)
            messages.append({'role': 'user', 'content': f"Image text: {image_text}"})

        response = openai.ChatCompletion.create(
            messages=messages,
            engine="gpt-35-turbo-16k-2",
            temperature=0,
        )

        return response.choices[0].message['content']

    st.sidebar.title("Brand Integrity Monitoring System")
    st.sidebar.image("ML.jpg", width=200)

    page = st.sidebar.selectbox("Select a page", ["Homepage", "Analyze for Fraud"])

    df = pd.read_csv('sample_tweets.csv')  # assuming your file is named 'sample_tweets.csv'

    if page == "Analyze for Fraud":
        tweet_index = st.selectbox("Select a tweet to analyze", options=range(df.shape[0]), format_func=lambda x: f"Tweet {x+1}")
        user_input = st.text_area("Enter your tweet here:", value=df.iloc[tweet_index]['tweet_text'] if df.shape[0] > tweet_index else "", key="tweet_input")
        image_data = st.file_uploader("Upload an image (optional)", type=["jpg", "png", "jpeg"])

        if st.button("Analyze"):
            if user_input or image_data:
                st.subheader("Analysis Result")
                result = generate_openai_response(user_input, image_data)
                st.write(result)
            else:
                st.warning("Please enter a tweet or upload an image for analysis.")

  

    elif page == "Homepage":
        st.header("The purpose of this App is to protect the customers from potential scammers marketing on behalf of reputed companies.")
        st.write("The digital age has seen a surge in online scams, especially in sectors like airlines, hotels, and transportation. These scams often manifest as too-good-to-be-true offers or deceptive promotions.")
        st.write("We all have come accross posts and advertisements offering extraordinary discounts that are not real and are placed for the purpose of extracting some valuable data from the customers like payment details, Membership details, etc.")
        st.write("Currently, there are no effective tools to automatically detect such fraudulent posts on social media and websites.")
        st.write("This tool is designed to identify between Fraud and Safe promotions based on various fraud indicators.")

        
        st.header("Categorised Output based on findings :")
        st.write("Fraud Alert V2 : 100% Fraud")
        st.write("Fraud Alert V1 : Highly to be a fraud")
        st.write("Looks Safe V1 : Looks pretty safe")
        st.write("Looks Safe V2 : 100% Safe")


        st.header("Current Scope and Technology used :")
        st.write("The current scope for this POC has been limited to Twitter for demonstration purposes.")
        st.write("The project’s current scope can be extended from Twitter to other social media platforms and websites, broadening the detection and prevention of online scams.")
        st.write("We initially started training LLM models like: LSTM and some other ML based decision making models like CNN and random forest. But, due to very limited data availabe to test and train the models and limited computer resources to keep training it for potential outcomes we decided to move to GPT models. Which were already trained on years of data and the efficiency was beyond comparision to other models. GPT4 was a clear winner for our usecases in terms of training and efficiency of results.")


        st.header("Training and Testing :")
        st.write("There were a sample of 200-300 tweets that was used to train the models. It was a mix sample of genuine and fraud tweets.")
        st.write("GPT models were trained on the basis of promt engineering to get desired results on top of the sample data")
        st.write("The model makes decision based on the following defined Fraud Indicators for desired output :")
        st.write("1) Keywords (Discount, Offers, Hurry, Claim, job opportunities) : Google Dorks and API calls")
        st.write("2) Public review websites : Web Scrape top review websites")
        st.write("3) Scan Social media account including posts and followers : API calls")
        st.write("4) Scam/Fraud reports on social media : API calls")
        st.write("5) Unusual Discount : Compare prices from original websites")
        st.write("6) Check URL for any similarities in name")
        st.write("7) Image processing and recognition for potential fraud content in the image.")
        st.write("8) Check the Domain/Account age : Wayback machine")
        st.write("9) Check Contact Information")
        st.write("10) Check for Privacy policy and terms of service")
        st.write("11) Check for digital certificates : SSL, DMARC, SPF, PKI")
        st.write("12)  Number and quality of Advertisements and Pop-ups")                

        st.header("Flowchart :")
        st.write("1) Someone tweets a fake promotion link for Delta Airlines")
        st.write("2) We collect the tweet based on the keywords using API calls")
        st.write("3) Pass the tweet contents to our bot")
        st.write("4) The bot analyzes the sentiment behind the tweet and also examines the URL's provided for any fraud related indicator")
        st.write("5) It converts the image data to text if any and passes it to the bot for analysis")
        st.write("6) Based on the contents of the tweet and the website the bot makes a decision and provides an explaination as to why the following tweet/URL looks like a fraud or safe.")
        st.write("7) It can work as a standalone tool on top of any cloud provider.")
        st.write("8) It can be integrated to company's existing website or social media platforms")
        st.write("9) Post the given output to social media handles,etc via API’s.")
       

        st.header("Potential Use cases :")
        st.write("The Driving force behind the development of our solution was to create a robust tool capable of safeguarding organizations against fraud schemes posted by third parties. This Solution is designed with the primary objective of preserving the integrity of businesses by offering a comprehensive defense mechanism against scams.")
        st.write("1) Used by brands to protect their reputation against potential fraud.")
        st.write("2) Detecting and Preventing Fake Airline/Hotel/Cruise ticket sales : Identifying fraudulent ticket offers on unautorized platforms, ensuring customers only purchase legit tickets through official channels.")
        st.write("3) The tool can be used to identify fake job opportunities and fake job postings on social media platforms.")
        st.write("4) The tool can be configured to identify Phishing emails and websites")
        st.write("5) Offers potential marketing opportunity for companies to help identify fraud and promote similar products.")
        st.write("6) The tool can also be configured to extract public reviews.")
        
        st.header("GPT 3.5 vs GPT 4 :")
        st.write("Limitiations of GPT 3.5 :")
        st.write("1) GPT4 is able to perform way better results than GPT3.5")
        st.write("2) GPT3.5 is not able to read the contents of the images, therefore we are currently using Python scripts to convert image data to text. DALLE is an alternate for this usecase to convert images to text through API calls and it have better efficiency than python scripts.")
        st.write("3) GPT3.5 does not have the ability to access websites in detail for further fraud analysis")
        st.write("4) We currently dont have access to GPT4 API, so we were training the GPT4 model online for our usecase and It provides way better results in terms of efficiency")


        st.header("Results, benifits and limitations :")
        st.write("We were able to train the GPT models for desired outcomes, it has the potential to understand the tweet for any fraud indicators and also to access the website provided in the link. It scans the website thoroughly for any fraud activites and also visit public review websites to extract any important fraud realated reviews there.")
        st.write("Currently the model is limited to analyse the text and image contents but it can be later extended to Videos and GIF's")



if __name__ == '__main__':
    main()
