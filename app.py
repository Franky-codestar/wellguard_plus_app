import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# 🔹 Set Page Config
st.set_page_config(page_title="WellGuard+ Analyzer", layout="wide")

st.title("🛡️ WellGuard+ | Group 1 Well Completion Analyzer")

# 🔹 Apply Background Image Styling (Ensuring Proper Detection)
bg_path = "background.png"
if os.path.exists(bg_path):
    st.image(bg_path, use_container_width=True)  # Direct Image Display
    st.markdown(
    f"""
    <style>
    .stApp {{
        background: url("background.png") no-repeat center center fixed;
        background-size: 25% auto;  /* Shrinks the image to half A4 size */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

else:
    st.warning(f"⚠️ Background image not found. Ensure '{bg_path}' is in your project folder.")

# 🔹 Hourly Data Options (User Must Manually Select Values)
time_stamps = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00"]
pressure_options = {
    "00:00": ["Select a value...", 1200, 1000],
    "01:00": ["Select a value...", 1180, 1480],
    "02:00": ["Select a value...", 1150, 1500],
    "03:00": ["Select a value...", 1120, 9000],
    "04:00": ["Select a value...", 1100, 1300],
    "05:00": ["Select a value...", 1070, 1080],
    "06:00": ["Select a value...", 1050, 1450],
    "07:00": ["Select a value...", 1020, 1022],
    "08:00": ["Select a value...", 980, 990],
    "09:00": ["Select a value...", 750, 950]
}
temperature_options = {
    "00:00": ["Select a value...", 68, 67],
    "01:00": ["Select a value...", 69, 65],
    "02:00": ["Select a value...", 70, 62],
    "03:00": ["Select a value...", 71, 82],
    "04:00": ["Select a value...", 72, 83],
    "05:00": ["Select a value...", 73, 84],
    "06:00": ["Select a value...", 74, 64],
    "07:00": ["Select a value...", 75, 64],
    "08:00": ["Select a value...", 76, 86],
    "09:00": ["Select a value...", 77, 87]
}
material_options = ["Select a material...", "Steel", "Composite", "Ceramic"]

# 🔹 User Input Section
selected_data = []
st.subheader("📊 Enter Hourly Pressure, Temperature & Material Data")
st.write("Select values below for pressure, temperature, and material type.")

for timestamp in time_stamps:
    st.markdown(f"**🕒 Timestamp: {timestamp}**")
    
    pressure_choice = st.selectbox(f"Pressure for {timestamp}", pressure_options[timestamp], key=f"pressure_{timestamp}")
    temperature_choice = st.selectbox(f"Temperature for {timestamp}", temperature_options[timestamp], key=f"temperature_{timestamp}")
    material_choice = st.selectbox(f"Material Type for {timestamp}", material_options, key=f"material_{timestamp}")

    selected_data.append({"Timestamp": timestamp, "Pressure": pressure_choice, "Temperature": temperature_choice, "Material": material_choice})

# 🔹 Convert Selections to DataFrame
df_selected = pd.DataFrame(selected_data)

# 🔹 Show Graph, Integrity Analysis & Material Suggestions ONLY if ALL selections are made
if all(val != "Select a value..." for val in df_selected["Pressure"]) and all(val != "Select a value..." for val in df_selected["Temperature"]) and all(val != "Select a material..." for val in df_selected["Material"]):
    st.subheader("📊 Pressure & Temperature Trends Over Time")
    fig, ax = plt.subplots()
    ax.plot(df_selected["Timestamp"], df_selected["Pressure"], label="Pressure (psi)", color="blue", marker="o")
    ax.plot(df_selected["Timestamp"], df_selected["Temperature"], label="Temperature (°C)", color="red", marker="s")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Values")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # 🔹 Integrity Analysis Display (Shown Alongside Graph)
    st.subheader("🛠️ Integrity Analysis")
    avg_pressure = df_selected["Pressure"].mean()
    avg_temperature = df_selected["Temperature"].mean()
    
    st.write(f"✅ **Average Pressure:** {avg_pressure:.2f} psi")
    st.write(f"✅ **Average Temperature:** {avg_temperature:.2f} °C")
    
    # Basic risk evaluation
    if avg_pressure > 2000 or avg_temperature > 85:
        st.warning("⚠️ **Potential Risk: Extreme conditions detected! Review mitigation strategies.**")
    else:
        st.success("✅ **Integrity Stable: No critical risks detected.**")

    # 🔹 Material Type Suggestions (Shown Alongside Graph & Integrity Analysis)
    st.subheader("📌 Material Selection Review")
    unsuitable_materials = df_selected[df_selected["Material"].isin(["Ceramic"])]

    if not unsuitable_materials.empty:
        st.warning("⚠️ Some selected materials may be unsuitable for high-pressure environments.")
        st.write("🔹 **Recommended Alternative:** Steel or Composite for enhanced durability.")

# 🔹 Admin Access Control with Passcode (Updated Message)
st.subheader("🔐 Admin Access")
admin_passcode = st.text_input("Enter Admin Passcode:", type="password")

if admin_passcode == "650560":
    st.success("✅ Access Granted: Viewing Admin Data")
    st.dataframe(df_selected)
else:
    st.warning("🔒 **Access Denied. Enter Passcode.**")