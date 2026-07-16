import os
import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Securely load API keys from the .env file
load_dotenv()

def generate_forensic_report(decrypted_threat_data):
    print("\n=========================================================")
    print(" [#GenerativeAI] INITIALIZING FORENSIC REPORTER (GEMINI)")
    print("=========================================================")

    # Securely fetch the Gemini key from your .env file
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY not found in .env file! Cannot generate report.")
        return

    # Configure the Gemini API client
    genai.configure(api_key=api_key)
    
    # Initialize the Gemini model (gemini-1.5-flash is extremely fast for text generation)
    model = genai.GenerativeModel('gemini-3.5-flash')

    # 1. Construct the AI Prompt using our decrypted threat intel
    prompt = f"""
    You are an elite Aerospace Cyber Security AI operating at the Bharat Space Education Research Centre (BSERC). 
    Generate a formal, human-readable forensic report based on the following intercepted orbital threat data. 
    The data was secured using Kyber-768 Post-Quantum Cryptography and AES-256 symmetric encryption on an Edge Computing Node.
    
    Keep the report professional, highly technical, and concise (under 200 words).

    Decrypted Space-Track Threat Data:
    {decrypted_threat_data}
    """

    try:
        print("   [SYSTEM] Transmitting decrypted intelligence to Gemini Generative AI model...")
        
        # Trigger the Gemini API
        response = model.generate_content(prompt)
        report = response.text

        # 2. Ensure the output logs/ directory exists to store SecOps outputs
        os.makedirs("logs", exist_ok=True)

        # 3. Save the forensic report to preserve the evidence
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"logs/Forensic_Report_{timestamp}.txt"
        
        with open(filename, "w") as f:
            f.write(report)

        print(f"   [SUCCESS] Gemini Forensic Report generated and securely archived to: {filename}")
        print("\n--- #ThreatIntelligence REPORT PREVIEW ---")
        print(report)
        print("------------------------------------------\n")

    except Exception as e:
        print(f"   [ERROR] Generative AI anomaly detected: {e}")