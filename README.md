# Writing Evaluator

## Overview

Writing Evaluator is a Streamlit-based web application that allows users to evaluate and analyze written works. It features author profiles, grading for each work, feedback visualization, and word clouds for text analysis. Users can also search for authors and view their work over time to track improvement.

## Features

- **Author Search**: Search for authors and view their written works.
- **Grading System**: View grades assigned to each written piece.
- **Feedback Visualization**: Analyze feedback and comments using visual tools.
- **Word Cloud Generation**: Generate a word cloud for each written piece to analyze common themes.
- **Performance Tracking**: Observe an author's progress over time.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/writing-evaluator.git
   ```
2. Navigate to the project directory:
   ```sh
   cd writing-evaluator
   ```
3. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the App

Run the following command:

```sh
streamlit run app.py
```

This will launch the application in your default web browser.

## Deployment

The application is deployed on [Streamlit Cloud](https://writingevaluator.streamlit.app/). If you push updates to the repo, follow these steps if the app does not reflect changes:

1. Restart the app from the Streamlit Cloud dashboard.
2. Clear the browser cache (`Ctrl + Shift + R`).
3. Run `git status` to ensure all changes are committed and pushed.

## Troubleshooting

- If the app is not updating on Streamlit Cloud, try:
  - Clearing Streamlit cache:
    ```python
    import streamlit as st
    st.cache_data.clear()
    st.cache_resource.clear()
    ```
  - Restarting the app from the Streamlit dashboard.
  - Checking logs for errors (`streamlit run app.py`).

## Contributing

Feel free to open issues or submit pull requests for bug fixes and feature improvements.

## License

This project is licensed under the MIT License.

---

