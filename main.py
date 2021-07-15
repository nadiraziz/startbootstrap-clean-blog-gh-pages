import smtplib

from flask import Flask, render_template, request
import requests

OWN_EMAIL = "nashshermi@gmail.com"
OWN_PASSWORD = "Azenco@7505"
app = Flask(__name__)
BLOG_API = "https://api.npoint.io/e42b353ee387383898c7"
posts = requests.get(BLOG_API).json()

@app.route('/')
def get_all_posts():
    return render_template("index.html", posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route('/about')
def about():
    return render_template("about.html")




@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)


if __name__ == '__main__':
    app.run(debug=True)
