# QuizVolution AI Unleashed

QuizVolution is an interactive, web-based quiz platform built with Flask. It allows users to test their programming knowledge across multiple languages and difficulty levels. Users can select their preferred languages, education level, and difficulty, and receive a personalized quiz. At the end, users get instant feedback, a detailed results page, and can download a PDF report of their performance. Optionally, results can be emailed directly to the user.

## Features

- Supports quizzes in C, C++, Java, Python, Go, React, HTML, CSS, JS, NodeJS, and Angular.
- Three difficulty levels: Easy, Intermediate, High.
- Personalized quiz experience based on user profile.
- Real-time feedback and explanations for each answer.
- Animated, modern UI with custom CSS and JavaScript.
- Downloadable PDF report of quiz performance.
- Option to receive results via email.

## Project Structure

```
app.py
flask_session/
static/
    css/
    js/
templates/
utils/
```

- `app.py`: Main Flask application and quiz logic.
- `static/`: Static assets (CSS, JS).
- `templates/`: HTML templates for quiz, results, and start page.
- `utils/email_sender.py`: Utility for sending quiz results via email.

## Getting Started

### Prerequisites

- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)
- [reportlab](https://pypi.org/project/reportlab/)
- [Flask](https://pypi.org/project/Flask/)
- [Flask-Session](https://pypi.org/project/Flask-Session/)

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/quizvolution.git
    cd quizvolution
    ```

2. Install dependencies:

    ```sh
    pip install Flask Flask-Session reportlab
    ```

3. Configure email sending:

    - Edit `utils/email_sender.py` and set your Gmail address and [App Password](https://support.google.com/accounts/answer/185833?hl=en) for the `sender` and `password` variables.

4. Run the app:

    ```sh
    python app.py
    ```

5. Open your browser and go to [http://localhost:5000](http://localhost:5000)

## Usage

1. Fill in your name, email, education level, select programming languages and difficulty.
2. Start the quiz and answer the questions.
3. View your results, download the PDF report, or receive results by email.

## License

This project is licensed under the MIT License.

---

**Enjoy learning and testing your programming skills with
