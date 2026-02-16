# 🌡️ Real-Time IoT Temperature & Humidity Monitor

Welcome! This project lets you build a professional-grade environment monitor that sends live data from your room to a beautiful website dashboard. 

**Think of it like this:** Your sensor "talks" to a computer in the cloud, and that computer "shouts" the information to your website dashboard instantly.

---

## 🛠️ Phase 1: The "Hardware" (The Physical Stuff)

You will need:
1. **ESP32 Development Board** (The "Brain")
2. **DHT11 Sensor** (The "Nose" that smells temperature and humidity)
3. **3 Jumper Wires** (The "Nerves" that connect the nose to the brain)
4. **USB Cable** (To give it power)

### 🔌 How to connect them (Wiring):
Look closely at your **DHT11 sensor**. It has 3 pins.
*   **Pin 1 (marked + or VCC):** Connect this to the **3V3** pin on your ESP32.
*   **Pin 2 (marked Out or Data):** Connect this to **Pin D4** on your ESP32.
*   **Pin 3 (marked - or GND):** Connect this to the **GND** pin on your ESP32.

---

## 💻 Phase 2: The "Backend" (The Cloud Brain)

We use a service called **Koyeb** to host the cloud brain.

1.  **Clone the project:** Download this code to your computer.
2.  **Upload to GitHub:** Create a new personal repository on GitHub and push this code there.
3.  **Koyeb Setup:**
    *   Create a free account on [Koyeb.com](https://www.koyeb.com/).
    *   Click **"Create Service"** -> **"GitHub"**.
    *   Select this repository.
    *   **Crucial Step:** In the "Environment Variables" section, add:
        *   `SENSOR_API_KEY`: Create a secret password (e.g., `my_secret_123`).
    *   Click **Deploy**.
    *   Once it's "Healthy," copy the **Public URL** (it looks like `https://...koyeb.app`).

---

## 🤖 Phase 3: The "ESP32 Code" (Teaching the Brain)

1.  Open **Arduino IDE** on your computer.
2.  Open the file `esp32_iot.ino`.
3.  **Fill in your details** at the top of the code:
    *   `ssid`: Your Wi-Fi name.
    *   `password`: Your Wi-Fi password.
    *   `serverName`: Paste your Koyeb URL and add `/sensor` at the end (e.g., `https://...koyeb.app/sensor`).
    *   `myApiKey`: Use the **same secret password** you created in Koyeb.
4.  **Install Libraries:** Go to `Tools -> Manage Libraries` and install:
    *   `DHT sensor library` by Adafruit.
    *   `ArduinoJson` by Benoit Blanchon.
5.  **Upload:** Plug in your ESP32 and click the **Upload** arrow.

---

## 📊 Phase 4: The "Dashboard" (The Visuals)

1.  Open `frontend/index.html`.
2.  Scroll to the bottom and find the line: `const socket = io("https://your-koyeb-app.koyeb.app");`
3.  Replace that URL with your actual Koyeb URL.
4.  **Host it:** You can upload just the `frontend` folder to [Vercel](https://vercel.com/) or [Netlify] for free.

---

## 🔐 Security (The "Shield")
I have built this project with a special "Secret Key" system. 
*   Because my repository is public, I have hidden my real Wi-Fi passwords and Cloud keys.
*   **Never share your real keys!** Always use Environment Variables on Koyeb to keep your project safe from hackers.

---

## ❓ Troubleshooting (If things go wrong)
*   **Error -11 on ESP32:** Check your Wi-Fi signal. Make sure your Koyeb server is "Healthy."
*   **Dashboad says "Connecting...":** Make sure the URL in `index.html` matches your Koyeb URL exactly.
*   **Funny symbols in Serial Monitor:** Make sure the speed is set to `115200 baud`.

**Now, sit back and watch your live data stream across the world! 🚀**
