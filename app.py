from flask import Flask, request, render_template_string
import pickle

app = Flask(__name__)

model = pickle.load(open("model.pkl","rb"))
vectorizer = pickle.load(open("vectorizer.pkl","rb"))

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

<p>Paste any news headline or article to check if it is real or fake.</p>

<form method="POST">
<textarea name="news" placeholder="Enter news text here..."></textarea>
<br>
<button type="submit">Analyze News</button>
</form>

{% if prediction %}
<div class="result">
Prediction:
<span class="{{'real' if prediction=='REAL' else 'fake'}}">
{{prediction}}
</span>
</div>
{% endif %}

<div class="footer">
Machine Learning Project • TF-IDF 
</div>

</div>

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def home():
    prediction=None

    if request.method=="POST":
        news=request.form["news"]
        vect=vectorizer.transform([news])
        prediction=model.predict(vect)[0]

    return render_template_string(html_page,prediction=prediction)

if __name__=="__main__":
    app.run(debug=True)