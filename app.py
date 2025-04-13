from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import openai

load_dotenv()
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-advice', methods=['POST'])
def get_advice():
    data = request.get_json()
    devices = data.get('devices', [])

    if not devices:
        return jsonify({'message': 'No devices provided.'}), 400

    formatted = '\n'.join(
        f"{d['name']} ({d['category']}): {d['watts']}W for {d['hours']} hours/day"
        for d in devices
    )

    prompt = f"""Here is a list of home appliances and their daily usage:
{formatted}

Give me tips to reduce electricity consumption based on this setup. Make it friendly and actionable."""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert energy advisor."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({'message': reply})
    except Exception as e:
        return jsonify({'message': 'Error from ChatGPT', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
