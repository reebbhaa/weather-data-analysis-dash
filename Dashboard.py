import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import warnings
import time
from wordcloud import WordCloud
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

# Configure NLTK data path
nltk.data.path.append(os.path.expanduser('~/nltk_data'))

# Download required NLTK data
nltk.download('punkt', quiet=True,
              download_dir=os.path.expanduser("~/nltk_data"))
nltk.download('punkt_tab', quiet=True,
              download_dir=os.path.expanduser("~/nltk_data"))
nltk.download('averaged_perceptron_tagger_eng', quiet=True,
              download_dir=os.path.expanduser("~/nltk_data"))

warnings.filterwarnings("ignore")

# Setting the title and page icon
st.set_page_config(
    page_title="Evaluator", page_icon=":material/grading:", layout="wide"
)


def authors():
    st.title("📚 Authors & Their Work")
    # Mock data - Replace with actual database query
    df = pd.DataFrame({
        "Author": ["Alice", "Bob", "Alice", "Charlie", "Bob"],
        "Title": ["Story 1", "Essay 1", "Story 2", "Poem 1", "Essay 2"],
        "Grade": [85, 90, 88, 75, 92],
        "Date": pd.to_datetime(["2024-01-01", "2024-01-10", "2024-02-15", "2024-03-01", "2024-04-05"])
    })
    # Search Bar on Main Page
    search_query = st.text_input("🔍 Search for an Author")

    # Filtering based on search query
    if search_query:
        filtered_authors = df[df["Author"].str.contains(
            search_query, case=False, na=False)]
        author_list = filtered_authors["Author"].unique()
    else:
        author_list = df["Author"].unique()

    # Filtering based on search query
    if search_query:
        filtered_authors = df[df["Author"].str.contains(
            search_query, case=False, na=False)]
        author_list = filtered_authors["Author"].unique()
    else:
        author_list = df["Author"].unique()

    # Filtering based on search query
    if search_query:
        author_data = df[df["Author"].str.contains(
            search_query, case=False, na=False)]
    else:
        author_data = df

    # Display Featured Authors (Top Performers)
    st.subheader("🌟 Featured Authors")
    top_authors = df.groupby("Author")["Grade"].mean().nlargest(3).index
    st.write(", ".join(top_authors))

    # Show Author Work Table
    st.subheader(f"Works by {search_query}" if search_query else "All Works")
    st.dataframe(author_data)

    # Show improvement if a single author is searched
    if search_query and not author_data.empty:
        st.subheader("📈 Grade Improvement Over Time")
        fig = px.line(author_data, x="Date", y="Grade",
                      title=f"{search_query}'s Grade Progress", markers=True)
        st.plotly_chart(fig)


def home():
    # st.title(":material/grading: Writing Evaluation")
    st.title("🏡 AI Writing Evaluator")
    st.subheader("Welcome to the 826 Valencia AI Writing Evaluator!")

    st.markdown(
        """
        Providing feedback on student writing is essential, but we know it can be time-consuming.
        This tool is designed to help **826 Valencia's staff and volunteers** efficiently assess writing samples while maintaining
        the personal touch that makes mentorship so valuable.

        With AI-powered evaluation, you can:  
        ✅ **Quickly analyze writing samples** based on 826 Valencia's grading rubric.  
        ✅ **Receive high-quality, personalized feedback** tailored to each student's strengths and areas for improvement.  
        ✅ **Save time and focus on mentorship** by reducing the administrative burden of grading.

        **Our goal?** To empower educators and volunteers with a **fast, easy-to-use, and cost-effective**
        solution for evaluating student writing, so you can spend more time inspiring creativity!
        
        - ------------------
        
        ## 📝 How It Works

        ### 1️⃣ Choose Your Upload Method:

        - **File Upload:** Upload a single student writing sample or multiple writing samples(.txt, .docx, .pdf).

        ### 2️⃣ AI-Powered Evaluation:

        - The tool will analyze writing based on 826 Valencia’s grading rubric.
        - It provides **structured scores** and **detailed feedback**, including actionable suggestions for improvement.

        ### 3️⃣ Review & Download Feedback:

        - View the results instantly on the platform.
        - Download feedback reports for individual or bulk submissions.

        ### 4️⃣ Use Feedback for Mentorship:

        - Share AI-generated insights with students.
        - Provide personalized guidance based on AI suggestions.
        """

    )


def writing_evaluation():
    st.title(":material/grading: Writing Evaluator")
    st.subheader(
        "Upload a file to evaluate the writing based on the 826 Valencia Rubric.")
    # Options to upload a file
    fl = st.file_uploader(":file_folder: Upload a file or multiple files.",
                          type=["pdf", "jpeg", "jpg", "png"])

    # TODO: Send files to the backend API
    # Simulated API response (Replace this with actual API call)
    if fl:
        st.info("Processing your file(s)... Please wait.")
        time.sleep(2)  # Simulating delay

        # Display results
        st.success("Evaluation Complete! Here are the results:")
        # Detect Streamlit Theme (Light/Dark Mode)
        theme = st.get_option("theme.base")
        light_mode = theme == "light"

        # Define rubric criteria based on 826 Valencia grading rubric
        rubric_criteria = [
            "Ideas", "Organization", "Voice", "Word Choice",
            "Sentence Fluency", "Conventions"
        ]

        # Mock evaluation results (Replace with real backend results)
        evaluation_results = {
            "Ideas": {"score": 5, "comment": "Strong ideas, but needs more supporting details."},
            "Organization": {"score": 4, "comment": "Well-structured, logical sequence of thoughts."},
            "Voice": {"score": 3, "comment": "Engaging but could be more distinctive."},
            "Word Choice": {"score": 2, "comment": "Good vocabulary but some repetitive words."},
            "Sentence Fluency": {"score": 3, "comment": "Smooth flow, but some choppy transitions."},
            "Conventions": {"score": 2, "comment": "Some grammar and punctuation errors."}
        }
        # Extract comments
        all_comments = " ".join([v["comment"]
                                for v in evaluation_results.values()])

        # Convert data to DataFrame for visualization
        df = pd.DataFrame(
            [(k, v["score"]) for k, v in evaluation_results.items()],
            columns=["Criterion", "Score"]
        )

        # 📝 Feedback Table
        st.subheader("💡 Feedback & Comments")

        # Apply dark mode or light mode styles dynamically
        table_bg_color = "#f4f4f4" if light_mode else "#333333"
        table_text_color = "#000000" if light_mode else "#f4f4f4"
        border_color = "#dddddd" if light_mode else "#555555"

        comments_html = f"""
        <style>
            table {{ width: 100%; border-collapse: collapse; font-size: 16px; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid {border_color}; }}
            th {{ background-color: {table_bg_color}; color: {table_text_color}; }}
            td {{ background-color: transparent; color: {table_bg_color}; }}
        </style>
        <table>
            <tr><th>Criterion</th><th>Score</th><th>Feedback</th></tr>
        """
        for criterion in rubric_criteria:
            score = evaluation_results[criterion]["score"]
            comment = evaluation_results[criterion]["comment"]
            comments_html += f"<tr><td><b>{criterion}</b></td><td>{score}</td><td>{comment}</td></tr>"
        comments_html += "</table>"

        st.markdown(comments_html, unsafe_allow_html=True)

        word_cloud(all_comments, light_mode)
        # 🎨 Bar Chart Visualization
        st.subheader("📊 Writing Evaluation Results")
        fig = px.bar(df, x="Criterion", y="Score", text="Score",
                     color="Score", color_continuous_scale="blues")
        fig.update_traces(textposition="outside")
        fig.update_layout(yaxis_range=[0, 5], height=400)
        st.plotly_chart(fig, use_container_width=True)


def word_cloud(all_comments, light_mode):

    # Tokenize words and identify adjectives
    words = word_tokenize(all_comments)
    tagged_words = nltk.pos_tag(words)  # POS tagging

    # List of positive adjectives (expandable)
    positive_adjectives = {
        "strong", "creative", "engaging", "good", "smooth",
        "clear", "logical", "distinctive", "visually", "improving",
        "excellent", "amazing", "fantastic", "brilliant", "creative",
        "engaging", "insightful", "clear", "strong", "persuasive",
        "compelling", "impressive", "remarkable", "eloquent", "thoughtful"
    }

    # Filter adjectives from comments
    filtered_words = [word for word, tag in tagged_words if tag in (
        "JJ", "JJR", "JJS") and word.lower() in positive_adjectives]

    # Generate Word Cloud
    wordcloud_text = " ".join(filtered_words)
    wordcloud = WordCloud(
        width=800, height=400, background_color="white" if light_mode else "white",
        colormap="Blues" if light_mode else "coolwarm"
    ).generate(wordcloud_text)

    # Display Word Cloud
    st.subheader("🌟 Word Cloud")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")  # Hide axes
    st.pyplot(fig)


def about():
    st.title("ℹ️ About")
    # Run function to display rubric
    display_rubric()
    # st.write("This is an app built with Streamlit.")


def contact():
    st.title("📞 Contact")
    st.write("Reach out at contact@example.com")


pg = st.navigation([
    st.Page(home, title="Home"),
    st.Page(authors, title="Authors"),
    st.Page(writing_evaluation, title="Evaluate"),
    st.Page(about, title="About"),
    st.Page(contact, title="Contact")
])


def display_rubric():
    st.title(":scroll: 826 Valencia Grading Rubric")
    st.subheader(
        "📖 This rubric outlines the key criteria for evaluating student writing.")

    # Define the rubric with CSS that adapts to light and dark mode
    rubric_html = """
    <style>
        /* Use Streamlit's built-in theme variables */
        :root {
            --background-light: #ffffff;
            --background-dark: #262730;
            --text-light: #000000;
            --text-dark: #ffffff;
            --border-light: #ddd;
            --border-dark: #444;
        }
        
        @media (prefers-color-scheme: dark) {
            table { background-color: var(--background-dark); color: var(--text-dark); }
            th, td { border-color: var(--border-dark); }
            th { background-color: #333; }
        }

        @media (prefers-color-scheme: light) {
            table { background-color: var(--background-light); color: var(--text-light); }
            th, td { border-color: var(--border-light); }
            th { background-color: #f4f4f4; }
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 16px;
            text-align: left;
        }
        th, td {
            border: 1px solid;
            padding: 12px;
            word-wrap: break-word;
        }
        td {
            vertical-align: top;
        }
    </style>
    
    <table>
        <tr>
            <th>Criterion</th>
            <th>Exceptional (5)</th>
            <th>Experienced (4)</th>
            <th>Proficient (3)</th>
            <th>Emerging (2)</th>
            <th>Beginning (1)</th>
        </tr>
        <tr>
            <td><b>Ideas & Content</b></td>
            <td>I have a clear, focused, important, and fully developed main idea, with original thoughts and opinions.</td>
            <td>I have a clear, focused, and fully developed main idea, but can share my own thoughts and opinions more creatively.</td>
            <td>I have a generally clear, focused, and accurate main idea, but I need to share creative ideas.</td>
            <td>I have a focus, but I need to make my main idea clearer.</td>
            <td>I started my writing, but I need to add ideas connected to the topic.</td>
        </tr>
        <tr>
            <td><b>Organization</b></td>
            <td>I have a clear purpose, satisfying conclusion, and use thoughtful, varied language to keep the reader's attention.</td>
            <td>I have a clear purpose throughout my writing and use transitions to connect different ideas, but my writing needs more variety. My ideas are separated into different paragraphs.</td>
            <td>I have sentences that make sense together, but I need to cover the main ideas clearly in paragraphs with purposeful transitions.</td>
            <td>I have sentences but I need to organize my ideas into a clear paragraph and add transitions. </td>
            <td>I have sentences, but I can organize them better so they make more sense. </td>
        </tr>
        <tr>
            <td><b>Voice</b></td>
            <td>I have a strong tone that supports my topic and engages the reader, and I consistently use a variety of techniques to enhance the flavor of my writing.</td>
            <td>I use a tone that supports my topic and engages my reader, but my writing needs to explore my perspective more and consider the audience.</td>
            <td>I have shown some of my personality and opinions, but I need to add more flavor and hook the reader more.</td>
            <td>I shared my opinion, but I can express how I feel about the topic better.</td>
            <td>I have sentences, but I need to express my opinion.</td>
        </tr>
        <tr>
            <td><b>Word Choice</b></td>
            <td>I use strong and specific words to create imagery for my reader, but I can add more powerful/varied  types of figurative language.</td>
            <td>I use a variety of vocabulary, but I can choose more specific words and figurative language to create an image in my reader's mind.</td>
            <td>I have juicy vocabulary that makes sense, but I can include some figurative language.</td>
            <td>I have some juicy words, but I can add more juicy words that fit.</td>
            <td>I have ideas, but I need to make sure I use the right words without repeating.</td>
        </tr>
        <tr>
            <td><b>Sentence Fluency</b></td>
            <td>I have well-structured sentences with strong rhythm and cadence, and I use varied words/phrases to enhance the flow of the overall writing.</td>
            <td>I have sentences with rhythm and my ideas flow well between one and the next, but I could use more complex sentences to move the piece forward.</td>
            <td>I have a variety of sentence beginnings, but I can create more variety in my sentence types for more flow and rhythm.</td>
            <td>I have sentences that make sense, but I can try using complex and compound sentences.</td>
            <td> have complete sentences, but they can be reorganized to help my reader understand them better.</td>
        </tr>
        <tr>
            <td><b>Conventions</b></td>
            <td>My writing is error-free and my choices in punctuation and grammar contribute to the creativity and clarity of the piece. </td>
            <td>I consistently use correct spelling, punctuation, and grammar, but could introduce a variety of punctuation.</td>
            <td>My sentences make sense. I have mostly used correct spelling and punctuation, but there are minor errors.</td>
            <td>I have sentences and the reader understands some of what I'm saying, but I have some errors that make my writing hard to understand.</td>
            <td>I have ideas, but I need to add periods and capital letters. </td>
        </tr>
    </table>
    """

    # Display the table in Streamlit
    st.markdown(rubric_html, unsafe_allow_html=True)


pg.run()
