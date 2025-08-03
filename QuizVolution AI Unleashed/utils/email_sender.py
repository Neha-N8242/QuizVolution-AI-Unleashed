import smtplib
from email.mime.text import MIMEText

def send_email(to_email, score, total, languages):
    sender = "eunoia7887@gmail.com"
    password = "your-app-password-here"  # Use Gmail App Password
    subject = "QuizVolution Results"
    body = f"Dear User,\n\nYou scored {score} out of {total} in your QuizVolution quiz.\nLanguages: {', '.join(languages)}\n\nThank you for participating!\nQuizVolution Team"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")