import requests
from flask import Flask, request, render_template_string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- APP ----------------
app = Flask(__name__)

# ---------------- API KEY ----------------
API_KEY = "53946c31a306a067aea76b83b701b5e3"

# ---------------- LIVE NEWS FUNCTION ----------------
def get_live_news(query="news"):
    url = f"http://api.mediastack.com/v1/news?access_key={API_KEY}&languages=en&limit=5&keywords={query}"
    
    response = requests.get(url)
    data = response.json()

    headlines = []

    if "data" in data:
        for item in data["data"][:5]:
            headlines.append(item["title"])

    return headlines


# ---------------- CHECK NEWS FUNCTION ----------------
def detect_news(user_news):
    headlines = get_live_news(user_news)

    if len(headlines) == 0:
        return "UNVERIFIED"

    texts = [user_news] + headlines

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(texts)

    score = cosine_similarity(tfidf[0:1], tfidf[1:]).max()

    if score > 0.30:
        return "REAL"
    else:
        return "FAKE"


# ---------------- HTML PAGE ----------------
html_page = """
<!DOCTYPE html>
<html>
<head>
<title>Fake News Detection</title>

<style>

body{
    margin:0;
    font-family:Arial, Helvetica, sans-serif;
    background:linear-gradient(135deg,#4facfe,#00f2fe);
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
}

.container{
    background:white;
    width:520px;
    padding:40px;
    border-radius:12px;
    box-shadow:0 15px 30px rgba(0,0,0,0.2);
    text-align:center;
}

h1{
    color:#333;
}

textarea{
    width:100%;
    height:120px;
    padding:12px;
    border-radius:8px;
    border:1px solid #ccc;
    font-size:14px;
    resize:none;
}

button{
    margin-top:15px;
    padding:12px 25px;
    border:none;
    border-radius:8px;
    background:#4facfe;
    color:white;
    font-size:16px;
    cursor:pointer;
}

button:hover{
    background:#2b8df6;
}

.result{
    margin-top:20px;
    font-size:22px;
    font-weight:bold;
}

.real{
    color:green;
}

.fake{
    color:red;
}

.unverified{
    color:orange;
}

.footer{
    margin-top:25px;
    font-size:13px;
    color:#777;
}

</style>
</head>

<body>

<div class="container">

<h1>Fake News Detection</h1>

<p>Paste any latest news headline or article to check if it is real or fake.</p>

<form method="POST">
<textarea name="news" placeholder="Enter news text here..."></textarea>
<br>
<button type="submit">Analyze News</button>
</form>

{% if prediction %}
<div class="result">
Prediction:
<span class="
{% if prediction=='REAL' %}
real
{% elif prediction=='FAKE' %}
fake
{% else %}
unverified
{% endif %}
">
{{prediction}}
</span>
</div>
{% endif %}

<div class="footer">
Live News AI Checker • MediaStack API
</div>

</div>

</body>
</html>
"""

# ---------------- ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None

    if request.method == "POST":
        news = request.form["news"]
        prediction = detect_news(news)

    return render_template_string(html_page, prediction=prediction)


# ---------------- RUN ----------------
if __name__ == "__main__":

    print("Latest Live News Predictions:")
    live_news = get_live_news()

    for news in live_news:
        result = detect_news(news)

        print(news)
        print("Prediction:", result)
        print("--------------------")

    app.run(debug=True)