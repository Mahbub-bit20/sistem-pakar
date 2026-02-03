# app.py
from flask import Flask, request, render_template_string
import json

app = Flask(__name__)

# Basis pengetahuan dari file JSON
with open("knowledge.json", "r", encoding="utf-8") as f:
    kb = json.load(f)

gejala = kb["gejala"]
aturan = kb["aturan"]

def forward_chaining(fakta):
    hasil = []
    for rule in aturan:
        cocok = [g for g in rule["if"] if g in fakta]
        persentase = (len(cocok) / len(rule["if"])) * 100
        if persentase > 0:
            hasil.append({
                "rule": rule["id"],
                "diagnosa": rule["then"],
                "gejala_cocok": [gejala[g] for g in cocok],
                "persentase": persentase
            })
    return hasil

TEMPLATE = """
<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <title>Sistem Pakar Hipertensi & Diabetes</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container py-5">
  <h2 class="mb-4">Konsultasi Gejala</h2>
  <form method="post">
    <div class="row">
      {% for k,v in gejala.items() %}
      <div class="col-md-6">
        <div class="form-check">
          <input class="form-check-input" type="checkbox" name="gejala" value="{{k}}" id="{{k}}">
          <label class="form-check-label" for="{{k}}">{{v}}</label>
        </div>
      </div>
      {% endfor %}
    </div>
    <button type="submit" class="btn btn-success mt-3">Diagnosa</button>
  </form>

  {% if hasil %}
  <div class="alert alert-info mt-4">
    <h4>Hasil Diagnosa:</h4>
    <ul>
    {% for h in hasil %}
      <li>
        <strong>{{h.diagnosa}}</strong> (Rule: {{h.rule}})<br>
        Gejala cocok: {{", ".join(h.gejala_cocok)}}<br>
        Persentase kecocokan: {{ "%.1f"|format(h.persentase) }}%
      </li>
    {% endfor %}
    </ul>
  </div>
  {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def index():
    fakta = request.form.getlist("gejala")
    hasil = forward_chaining(fakta) if fakta else []
    return render_template_string(TEMPLATE, gejala=gejala, hasil=hasil)

if __name__ == "__main__":
    app.run(debug=True)