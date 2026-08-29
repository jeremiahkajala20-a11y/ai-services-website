import os
import requests
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ==================== DEEPSEEK AI ====================
# BADILISHA HII NA API KEY YAKO HALISI
DEEPSEEK_API_KEY = "sk-your-api-key-here"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_WEBSITE = "https://www.deepseek.com/en/"

# ==================== DATA ====================
TRAINING_DATA = {
    "computer_basics": {
        "title": "Misingi ya Kompyuta",
        "icon": "💻",
        "color": "#6366f1",
        "steps": [
            {"step": "Kuwasha na kuzima kompyuta vizuri", "tip": "Tumia Start Menu > Shut Down"},
            {"step": "Kutumia keyboard na mouse", "tip": "Jifunze shortcuts muhimu"},
            {"step": "Kufungua na kuhifadhi faili", "tip": "Ctrl+O kufungua, Ctrl+S kuhifadhi"}
        ]
    },
    "microsoft_office": {
        "title": "Microsoft Office",
        "icon": "📊",
        "color": "#22c55e",
        "steps": [
            {"step": "Microsoft Word - Kuandika na kuhifadhi hati", "tip": "Ctrl+S kuhifadhi mara kwa mara"},
            {"step": "Microsoft Excel - Kuunda meza na hesabu", "tip": "Tumia formula =SUM()"},
            {"step": "Microsoft PowerPoint - Kuunda presentation", "tip": "Slide design ni muhimu"}
        ],
        "shortcuts": [
            "Ctrl+C = Kunakili", "Ctrl+V = Kubandika",
            "Ctrl+B = Bold", "Ctrl+I = Italic",
            "Ctrl+S = Kuhifadhi", "Ctrl+P = Kuchapisha"
        ]
    },
    "internet_safety": {
        "title": "Usalama wa Mtandao",
        "icon": "🔒",
        "color": "#f59e0b",
        "steps": [
            {"step": "Tumia nenosiri imara", "tip": "Herufi kubwa, ndogo, namba na alama"},
            {"step": "Usibonyeze viungo vya tuhuma", "tip": "Angalia URL kabla ya kubonyeza"},
            {"step": "Usishiriki taarifa za siri mtandaoni", "tip": "Data yako ni mali yako"}
        ]
    }
}

SERVICES = [
    {
        "id": "online_learning",
        "icon": "fa-graduation-cap",
        "title": "Online Learning Skills",
        "description": "Jifunze ujuzi wa kompyuta mtandaoni kwa bei nafuu",
        "features": ["Mafunzo ya Microsoft Office", "Mafunzo ya simu na laptop", "Mafunzo ya usalama wa mtandao"],
        "price": "Kuanzia TSh 10,000"
    },
    {
        "id": "delivery",
        "icon": "fa-truck",
        "title": "Delivery Service (Bukoba)",
        "description": "Tunafanya delivery ya vifaa vyovyote Bukoba Mjini",
        "features": ["Bukoba Mjini - Sehemu zote", "Hospitali ya Bukoba (Ruka)", "Ofisi na makazi yoyote"],
        "price": "TSh 2,000 - 10,000"
    },
    {
        "id": "stationary",
        "icon": "fa-book",
        "title": "Moving & Static Stationary",
        "description": "Tunauza vifaa vya stationary na kufanya moving services",
        "features": ["Uuzaji wa kalamu, daftari, karatasi", "Uchapishaji wa hati", "Moving services"],
        "price": "Kuanzia TSh 1,000"
    },
    {
        "id": "device_advice",
        "icon": "fa-mobile-screen",
        "title": "Ushauri wa Devices",
        "description": "Tunatoa ushauri wa kitaalamu kuhusu simu na laptop",
        "features": ["Ushauri wa aina ya simu/laptop", "Ushauri wa specs na bei", "Ushauri wa matengenezo"],
        "price": "Ushauri bure"
    },
    {
        "id": "device_delivery",
        "icon": "fa-box",
        "title": "Delivery ya Simu na Laptop",
        "description": "Tunauza na kufanya delivery ya simu na laptop",
        "features": ["Simu mpya na zilizotumika", "Laptop mpya na zilizotumika", "Accessories"],
        "price": "Bei nafuu"
    },
    {
        "id": "it_support",
        "icon": "fa-tools",
        "title": "IT Support & Troubleshooting",
        "description": "Tunasaidia wanaopata changamoto kwenye simu na laptop",
        "features": ["Kusaidia kurekebisha matatizo", "Kusaidia kusakinisha programu", "Kusaidia kufungua akaunti"],
        "price": "TSh 5,000 - 15,000"
    },
    {
        "id": "word_typing",
        "icon": "fa-file-pen",
        "title": "Word Typing Services",
        "description": "Tunaandika barua, hati, na documentation zote",
        "features": ["Kuandika barua za kazi", "Kuandika hati na mikataba", "Kuandika CV"],
        "price": "Kuanzia TSh 2,000"
    }
]

VIDEO_RESOURCES = [
    {"title": "Bro Code - Programming Tutorials", "description": "Mafunzo kamili ya Python, JavaScript, C++", "url": "https://www.youtube.com/@BroCodez", "icon": "fa-code", "source": "YouTube"},
    {"title": "freeCodeCamp - Full Courses", "description": "Kozi kamili za bure za programming na IT", "url": "https://www.youtube.com/@freecodecamp", "icon": "fa-laptop-code", "source": "YouTube"},
    {"title": "Traversy Media - Web Development", "description": "Mafunzo ya kisasa ya web development", "url": "https://www.youtube.com/@TraversyMedia", "icon": "fa-globe", "source": "YouTube"},
    {"title": "Programming with Mosh", "description": "Mafunzo ya programming kwa urahisi", "url": "https://www.youtube.com/@programmingwithmosh", "icon": "fa-graduation-cap", "source": "YouTube"},
    {"title": "TechWorld with Nana - DevOps", "description": "Mafunzo ya DevOps, Docker, Kubernetes", "url": "https://www.youtube.com/@TechWorldwithNana", "icon": "fa-cloud", "source": "YouTube"},
    {"title": "Alex The Analyst - Data Analysis", "description": "Mafunzo ya data analysis na SQL", "url": "https://www.youtube.com/@AlexTheAnalyst", "icon": "fa-chart-bar", "source": "YouTube"}
]

# ==================== ROUTES ====================

@app.route("/")
def index():
    return render_template("index.html", 
        topics=TRAINING_DATA, 
        services=SERVICES,
        videos=VIDEO_RESOURCES,
        deepseek_url=DEEPSEEK_WEBSITE
    )

@app.route("/topic/<topic_name>")
def topic(topic_name):
    if topic_name in TRAINING_DATA:
        return render_template("topic.html", data=TRAINING_DATA[topic_name])
    return jsonify({"error": "Mada haipatikani"}), 404

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form.get("user_input", "").strip()
    
    if not user_input:
        return jsonify({"response": "Tafadhali andika swali lako."})
    
    # Jaribu DeepSeek AI
    if DEEPSEEK_API_KEY and DEEPSEEK_API_KEY != "sk-your-api-key-here":
        try:
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Wewe ni mwalimu wa IT unawafundisha Watanzania kwa Kiswahili."},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            response = requests.post(DEEPSEEK_API_URL, json=data, headers=headers, timeout=30)
            if response.status_code == 200:
                result = response.json()["choices"][0]["message"]["content"]
                return jsonify({"response": result, "ai": "DeepSeek"})
        except Exception as e:
            # Ikiwa DeepSeek inakosea, endelea na majibu ya msingi
            pass
    
    # Fallback - Majibu ya msingi
    return jsonify({
        "response": """📚 **Mwalimu wa IT**

Swali lako limepokelewa!

✅ Kwa msaada, wasiliana nami:
📞 RAMADHAN KAJALA - 0748755636
💬 WhatsApp: 0748755636

🌟 **Huduma Zetu:**
🎓 Online Learning Skills
🚚 Delivery Service (Bukoba)
📚 Moving & Static Stationary
📱 Ushauri wa Devices
📦 Delivery ya Simu na Laptop
🛠️ IT Support
📝 Word Typing Services

📺 Tazama mafunzo ya video kwenye sehemu ya Video Resources.

Nitakusaidia haraka! 💪""",
        "ai": "Offline"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
