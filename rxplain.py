import http.server
import json
import urllib.request
import base64
import os

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>RxPlain — Medicine Explainer</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet"/>
<style>
  :root {
    --green: #1a6b4a;
    --green-light: #e8f5ef;
    --green-mid: #2d9b6f;
    --cream: #faf8f3;
    --text: #1a1a1a;
    --muted: #6b7280;
    --red: #dc2626;
    --orange: #d97706;
    --blue: #1d4ed8;
    --card: #ffffff;
    --border: #e5e0d8;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'DM Sans', sans-serif;
    background: var(--cream);
    color: var(--text);
    min-height: 100vh;
  }

  /* Decorative background */
  body::before {
    content: '';
    position: fixed;
    top: -200px; right: -200px;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(45,155,111,0.08) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
  }

  header {
    background: var(--green);
    padding: 18px 32px;
    display: flex;
    align-items: center;
    gap: 14px;
    box-shadow: 0 2px 20px rgba(26,107,74,0.3);
    position: relative;
    z-index: 10;
  }

  .logo-icon {
    width: 44px; height: 44px;
    background: white;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
  }

  .logo-text {
    display: flex; flex-direction: column;
  }

  .logo-title {
    font-family: 'DM Serif Display', serif;
    color: white;
    font-size: 24px;
    line-height: 1;
    letter-spacing: -0.5px;
  }

  .logo-sub {
    color: rgba(255,255,255,0.7);
    font-size: 12px;
    font-weight: 300;
    letter-spacing: 0.5px;
  }

  .badge {
    margin-left: auto;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3);
    color: white;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.5px;
  }

  main {
    max-width: 720px;
    margin: 0 auto;
    padding: 40px 20px 60px;
    position: relative;
    z-index: 1;
  }

  .hero {
    text-align: center;
    margin-bottom: 36px;
  }

  .hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 36px;
    color: var(--green);
    line-height: 1.2;
    margin-bottom: 10px;
  }

  .hero h1 em {
    font-style: italic;
    color: var(--green-mid);
  }

  .hero p {
    color: var(--muted);
    font-size: 15px;
    font-weight: 300;
    max-width: 420px;
    margin: 0 auto;
    line-height: 1.6;
  }

  /* Upload zone */
  .upload-card {
    background: var(--card);
    border: 2px dashed var(--border);
    border-radius: 20px;
    padding: 40px 30px;
    text-align: center;
    cursor: pointer;
    transition: all 0.25s;
    position: relative;
    margin-bottom: 20px;
  }

  .upload-card:hover, .upload-card.drag {
    border-color: var(--green-mid);
    background: var(--green-light);
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(26,107,74,0.12);
  }

  .upload-icon {
    font-size: 48px;
    margin-bottom: 14px;
    display: block;
  }

  .upload-card h3 {
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 6px;
    color: var(--text);
  }

  .upload-card p {
    color: var(--muted);
    font-size: 13px;
  }

  #fileInput { display: none; }

  /* Language selector */
  .lang-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
    flex-wrap: wrap;
  }

  .lang-label {
    font-size: 13px;
    font-weight: 500;
    color: var(--muted);
    white-space: nowrap;
  }

  .lang-btn {
    padding: 6px 14px;
    border-radius: 20px;
    border: 1.5px solid var(--border);
    background: white;
    font-family: 'DM Sans', sans-serif;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    color: var(--text);
  }

  .lang-btn.active, .lang-btn:hover {
    background: var(--green);
    border-color: var(--green);
    color: white;
  }

  /* Preview */
  #preview {
    display: none;
    margin-bottom: 20px;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    position: relative;
  }

  #preview img {
    width: 100%;
    max-height: 280px;
    object-fit: contain;
    background: #f0f0f0;
    display: block;
  }

  .preview-label {
    position: absolute;
    top: 12px; left: 12px;
    background: var(--green);
    color: white;
    font-size: 11px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 10px;
    letter-spacing: 0.5px;
  }

  /* Analyze button */
  #analyzeBtn {
    display: none;
    width: 100%;
    padding: 16px;
    background: var(--green);
    color: white;
    border: none;
    border-radius: 14px;
    font-family: 'DM Sans', sans-serif;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.25s;
    letter-spacing: 0.3px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
  }

  #analyzeBtn:hover {
    background: #15573c;
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(26,107,74,0.35);
  }

  #analyzeBtn:active { transform: translateY(0); }

  #analyzeBtn:disabled {
    background: var(--muted);
    cursor: not-allowed;
    transform: none;
  }

  /* Loading */
  .loading {
    display: none;
    text-align: center;
    padding: 40px 20px;
  }

  .pulse-ring {
    width: 60px; height: 60px;
    border-radius: 50%;
    border: 3px solid var(--green-light);
    border-top-color: var(--green);
    animation: spin 1s linear infinite;
    margin: 0 auto 16px;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  .loading p {
    color: var(--muted);
    font-size: 14px;
  }

  .loading strong {
    display: block;
    color: var(--green);
    font-size: 16px;
    margin-bottom: 4px;
  }

  /* Result card */
  #result {
    display: none;
    background: var(--card);
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 4px 30px rgba(0,0,0,0.08);
    border: 1px solid var(--border);
  }

  .result-header {
    background: var(--green);
    padding: 18px 24px;
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .result-header span {
    font-size: 24px;
  }

  .result-header div {
    color: white;
  }

  .result-header h3 {
    font-family: 'DM Serif Display', serif;
    font-size: 20px;
    font-weight: 400;
  }

  .result-header p {
    font-size: 12px;
    opacity: 0.75;
    margin-top: 2px;
  }

  .result-body {
    padding: 24px;
  }

  /* Section blocks */
  .info-block {
    margin-bottom: 18px;
    padding: 16px 18px;
    border-radius: 12px;
    border-left: 4px solid;
  }

  .info-block.green {
    background: var(--green-light);
    border-color: var(--green);
  }

  .info-block.orange {
    background: #fff7ed;
    border-color: var(--orange);
  }

  .info-block.red {
    background: #fef2f2;
    border-color: var(--red);
  }

  .info-block.blue {
    background: #eff6ff;
    border-color: var(--blue);
  }

  .block-title {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .info-block.green .block-title { color: var(--green); }
  .info-block.orange .block-title { color: var(--orange); }
  .info-block.red .block-title { color: var(--red); }
  .info-block.blue .block-title { color: var(--blue); }

  .block-content {
    font-size: 14px;
    line-height: 1.7;
    color: var(--text);
    white-space: pre-wrap;
  }

  /* Disclaimer */
  .disclaimer {
    margin-top: 20px;
    padding: 14px 18px;
    background: #f9fafb;
    border-radius: 10px;
    font-size: 11px;
    color: var(--muted);
    line-height: 1.6;
    display: flex;
    gap: 8px;
    align-items: flex-start;
  }

  /* Try again */
  #tryAgain {
    display: none;
    margin-top: 16px;
    width: 100%;
    padding: 12px;
    background: transparent;
    border: 2px solid var(--green);
    color: var(--green);
    border-radius: 12px;
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }

  #tryAgain:hover {
    background: var(--green-light);
  }

  /* Error */
  #error {
    display: none;
    background: #fef2f2;
    border: 1px solid #fca5a5;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    color: var(--red);
    margin-bottom: 16px;
  }

  /* Offline badge */
  .offline-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--green-light);
    border: 1px solid rgba(26,107,74,0.2);
    color: var(--green);
    font-size: 12px;
    font-weight: 500;
    padding: 5px 12px;
    border-radius: 20px;
    margin-bottom: 24px;
  }

  .dot {
    width: 7px; height: 7px;
    background: var(--green-mid);
    border-radius: 50%;
    animation: blink 2s ease-in-out infinite;
  }

  @keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }
</style>
</head>
<body>

<header>
  <div class="logo-icon">💊</div>
  <div class="logo-text">
    <div class="logo-title">RxPlain</div>
    <div class="logo-sub">Medicine Explained Simply</div>
  </div>
  <div class="badge">🔒 100% Private • Runs Locally</div>
</header>

<main>
  <div class="hero">
    <h1>Understand your<br/><em>medicine</em> in seconds</h1>
    <p>Upload a photo of any medicine strip, tablet, or prescription — we'll explain it in plain language you understand.</p>
  </div>

  <div style="text-align:center;">
    <div class="offline-pill">
      <div class="dot"></div>
      Powered by Gemma 3 · Runs on your device · No data sent anywhere
    </div>
  </div>

  <!-- Language selector -->
  <div class="lang-row">
    <span class="lang-label">🌐 Explain in:</span>
    <button class="lang-btn active" onclick="setLang(this,'English')">English</button>
    <button class="lang-btn" onclick="setLang(this,'Hindi')">हिंदी</button>
    <button class="lang-btn" onclick="setLang(this,'Urdu')">اردو</button>
    <button class="lang-btn" onclick="setLang(this,'Tamil')">தமிழ்</button>
    <button class="lang-btn" onclick="setLang(this,'Bengali')">বাংলা</button>
    <button class="lang-btn" onclick="setLang(this,'Arabic')">العربية</button>
    <button class="lang-btn" onclick="setLang(this,'Spanish')">Español</button>
    <button class="lang-btn" onclick="setLang(this,'French')">Français</button>
  </div>

  <!-- Upload zone -->
  <div class="upload-card" id="uploadZone" onclick="document.getElementById('fileInput').click()"
       ondragover="event.preventDefault();this.classList.add('drag')"
       ondragleave="this.classList.remove('drag')"
       ondrop="handleDrop(event)">
    <span class="upload-icon">📷</span>
    <h3>Tap to upload medicine photo</h3>
    <p>Medicine strip · Tablet box · Prescription · Blister pack</p>
    <input type="file" id="fileInput" accept="image/*" capture="environment" onchange="handleFile(event)"/>
  </div>

  <!-- Preview -->
  <div id="preview">
    <div class="preview-label">📸 UPLOADED</div>
    <img id="previewImg" src="" alt="Medicine preview"/>
  </div>

  <!-- Analyze button -->
  <button id="analyzeBtn" onclick="analyze()">🔍 Explain This Medicine</button>

  <!-- Loading -->
  <div class="loading" id="loading">
    <div class="pulse-ring"></div>
    <strong>Gemma is reading your medicine...</strong>
    <p>Analyzing ingredients, uses & warnings</p>
  </div>

  <!-- Error -->
  <div id="error"></div>

  <!-- Result -->
  <div id="result">
    <div class="result-header">
      <span>💊</span>
      <div>
        <h3 id="medicineName">Medicine Information</h3>
        <p id="medicineType">Analysis complete</p>
      </div>
    </div>
    <div class="result-body">
      <div class="info-block green">
        <div class="block-title">✅ What is this medicine?</div>
        <div class="block-content" id="whatIs"></div>
      </div>
      <div class="info-block blue">
        <div class="block-title">💡 What is it used for?</div>
        <div class="block-content" id="usedFor"></div>
      </div>
      <div class="info-block orange">
        <div class="block-title">⚠️ Side effects</div>
        <div class="block-content" id="sideEffects"></div>
      </div>
      <div class="info-block red">
        <div class="block-title">🚫 Warnings</div>
        <div class="block-content" id="warnings"></div>
      </div>
      <div class="info-block blue">
        <div class="block-title">📋 How to take it</div>
        <div class="block-content" id="howToTake"></div>
      </div>
      <div class="disclaimer">
        ⚕️ <span>This is for general awareness only. Always follow your doctor's prescription and consult a licensed pharmacist or physician before taking any medicine.</span>
      </div>
    </div>
  </div>

  <button id="tryAgain" onclick="reset()">📷 Scan Another Medicine</button>
</main>

<script>
  let selectedLang = 'English';
  let imageBase64 = '';

  function setLang(btn, lang) {
    document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    selectedLang = lang;
  }

  function handleFile(event) {
    const file = event.target.files[0];
    if (file) loadImage(file);
  }

  function handleDrop(event) {
    event.preventDefault();
    document.getElementById('uploadZone').classList.remove('drag');
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) loadImage(file);
  }

  function loadImage(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      imageBase64 = e.target.result.split(',')[1];
      document.getElementById('previewImg').src = e.target.result;
      document.getElementById('preview').style.display = 'block';
      document.getElementById('analyzeBtn').style.display = 'block';
      document.getElementById('uploadZone').style.display = 'none';
    };
    reader.readAsDataURL(file);
  }

  async function analyze() {
    document.getElementById('analyzeBtn').style.display = 'none';
    document.getElementById('loading').style.display = 'block';
    document.getElementById('result').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    document.getElementById('tryAgain').style.display = 'none';

    const prompt = `You are a helpful medical assistant. Look at this medicine image carefully.

Please respond ONLY in ${selectedLang} language (translate everything including labels).

Identify the medicine and provide this information in a warm, simple way a patient with no medical knowledge can understand:

MEDICINE_NAME: [name of the medicine]
MEDICINE_TYPE: [e.g. antibiotic, painkiller, vitamin]
WHAT_IS_IT: [2-3 sentences explaining what this medicine is in very simple words]
USED_FOR: [what conditions/symptoms it treats, in simple language]
SIDE_EFFECTS: [common side effects, listed simply]
WARNINGS: [important warnings - who should NOT take it, drug interactions, pregnancy etc]
HOW_TO_TAKE: [general guidance on dosage timing, with/without food etc]

If you cannot identify the medicine clearly from the image, say so honestly and ask the patient to show the full box or prescription to their pharmacist.`;

    try {
      const response = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: imageBase64, prompt: prompt })
      });

      const data = await response.json();

      if (data.error) throw new Error(data.error);

      const text = data.result;

      // Parse sections
      document.getElementById('medicineName').textContent =
        extract(text, 'MEDICINE_NAME') || 'Medicine Analysis';
      document.getElementById('medicineType').textContent =
        extract(text, 'MEDICINE_TYPE') || 'Analysis complete';
      document.getElementById('whatIs').textContent =
        extract(text, 'WHAT_IS_IT') || text;
      document.getElementById('usedFor').textContent =
        extract(text, 'USED_FOR') || '—';
      document.getElementById('sideEffects').textContent =
        extract(text, 'SIDE_EFFECTS') || '—';
      document.getElementById('warnings').textContent =
        extract(text, 'WARNINGS') || '—';
      document.getElementById('howToTake').textContent =
        extract(text, 'HOW_TO_TAKE') || '—';

      document.getElementById('loading').style.display = 'none';
      document.getElementById('result').style.display = 'block';
      document.getElementById('tryAgain').style.display = 'block';

    } catch (err) {
      document.getElementById('loading').style.display = 'none';
      document.getElementById('error').style.display = 'block';
      document.getElementById('error').innerHTML =
        '❌ <strong>Error:</strong> ' + err.message + '<br/><small>Make sure Ollama is running with gemma3 model.</small>';
      document.getElementById('analyzeBtn').style.display = 'block';
    }
  }

  function extract(text, key) {
    const regex = new RegExp(key + ':\\s*([\\s\\S]*?)(?=\\n[A-Z_]+:|$)');
    const match = text.match(regex);
    return match ? match[1].trim() : null;
  }

  function reset() {
    document.getElementById('preview').style.display = 'none';
    document.getElementById('analyzeBtn').style.display = 'none';
    document.getElementById('result').style.display = 'none';
    document.getElementById('tryAgain').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    document.getElementById('uploadZone').style.display = 'block';
    document.getElementById('fileInput').value = '';
    imageBase64 = '';
  }
</script>
</body>
</html>"""


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress logs

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML.encode())

    def do_POST(self):
        if self.path == '/analyze':
            length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(length))

            try:
                payload = {
                    "model": "gemma3",
                    "prompt": body['prompt'],
                    "images": [body['image']],
                    "stream": False
                }

                req = urllib.request.Request(
                    'http://localhost:11434/api/generate',
                    data=json.dumps(payload).encode(),
                    headers={'Content-Type': 'application/json'}
                )

                with urllib.request.urlopen(req, timeout=120) as resp:
                    result = json.loads(resp.read())
                    answer = result.get('response', 'Could not analyze the image.')

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'result': answer}).encode())

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())


print("=" * 50)
print("  💊 RxPlain is starting...")
print("  Open your browser and go to:")
print("  http://localhost:8080")
print("=" * 50)

server = http.server.HTTPServer(('localhost', 8080), Handler)
server.serve_forever()
