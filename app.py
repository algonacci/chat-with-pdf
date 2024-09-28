import os
from flask import Flask, request, render_template, jsonify
from embedchain import App

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)
RAG_app = App.from_config(config_path="config.yaml")

UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if request.method == "POST":
        file = request.files['pdfFile']
        if file and file.filename.endswith('.pdf'):
                try:
                    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                    file.save(file_path)

                    RAG_app.add("pdf_file", file_path),

                    return render_template("chat.html")
                
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
        else:
                return jsonify({"error": "Only PDF files are allowed"}), 400


@app.route("/rag")
def rag():
    msg = request.args.get('msg')
    result, sources = RAG_app.query(msg, citations=True)
    return jsonify({
            "status": {
                "code": 200,
                "message": "Success generating response"
            },
            "data": {
                "result": result,
                "sources": sources,
            }
        })



if __name__ == "__main__":
    app.run()