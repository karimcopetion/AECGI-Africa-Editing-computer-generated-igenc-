import streamlit as st
import requests
import time
import os

# =================================================================
# 🔐 ACQUIRING API KEY VIA RENDER ENVIRONMENT (SAFE & SECURE)
# =================================================================
REPLICATE_API_KEY = os.environ.get("REPLICATE_API_KEY")

# --- 1. DESIGN N'ISHUSHO YA WEBSITE (UI CONFIG) ---
st.set_page_config(
    page_title="AECGI Secure AI Engine", 
    page_icon="🎬", 
    layout="wide"
)

st.title("🎬 AECGI ULTIMATE AI VIDEO ENGINE v17.0")
st.subheader("Hollywood-Grade Animation Studio (Secure Node)")
st.write("Urubuga rwuzuye rwo Gukora Video z'Iminota n'Amasegonda Ukokesheje AI")

st.markdown("---")

# --- 2. SIDEBAR STATUS ---
st.sidebar.header("⚙️ AECGI Core Status")
if REPLICATE_API_KEY:
    st.sidebar.success("✅ SYSTEM STATUS: SECURELY CONNECTED")
else:
    st.sidebar.error("❌ SYSTEM STATUS: MISSING REPLICATE_API_KEY IN RENDER")
st.sidebar.markdown("---")

# --- 3. THE MAIN VIDEO ENGINE ---
st.header("🎞️ Generator & Prompt Studio")
ai_editing_prompt = st.text_area(
    "Andika Prompt ya Video hano (Mu Cyongereza):",
    placeholder="A high-speed tactical Jeep Trackhawk racing through Kigali streets, cars with guns attached shooting, massive Hollywood explosions, cinematic lighting, 4k resolution, photorealistic CGI..."
)

st.markdown("###")

# --- 4. TANGIRA GUKORA VIDEO ---
if st.button("🚀 Tangira Gukora Video / Render CGI") and ai_editing_prompt:
    if not REPLICATE_API_KEY:
        st.error("⚠️ Umwubatsi Mukuru, ntabwo urashyira REPLICATE_API_KEY muli Settings za Render!")
    else:
        with st.spinner("AECGI AI Core iri gukorana na Server za Replicate... Tegereza gato..."):
            try:
                headers = {
                    "Authorization": f"Token {REPLICATE_API_KEY}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "version": "392f6699127431114346340426d7b21efc163a1211bc99734a1d831b26551b74", 
                    "input": {
                        "prompt": ai_editing_prompt,
                        "num_frames": 14,
                        "fps": 6
                    }
                }
                
                response = requests.post("https://api.replicate.com/v1/predictions", headers=headers, json=data)
                res_json = response.json()
                
                prediction_id = res_json.get("id")
                
                if prediction_id:
                    status = "starting"
                    ai_video_url = ""
                    
                    while status not in ["succeeded", "failed"]:
                        time.sleep(4)
                        check_res = requests.get(f"https://api.replicate.com/v1/predictions/{prediction_id}", headers=headers)
                        status = check_res.json().get("status")
                        
                        if status == "succeeded":
                            ai_video_url = check_res.json().get("output")
                            break
                        elif status == "failed":
                            break
                    
                    if ai_video_url:
                        st.success("✅ Video yawe ya CGI iruzuye neza!")
                        if isinstance(ai_video_url, list):
                            st.video(ai_video_url[0])
                        else:
                            st.video(ai_video_url)
                        st.balloons()
                    else:
                        st.error("⚠️ Server yanze gupfunda video. Ongera ugerageze gato.")
                else:
                    st.error("⚠️ API Key iri muli Render ntabwo ari nziza. Genzura niba ari nshya.")
            except Exception as e:
                st.error(f"⚠️ Haza ikosa mu mivugururire ya System: {e}")
