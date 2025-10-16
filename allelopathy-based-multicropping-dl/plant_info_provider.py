import streamlit as st
import pandas as pd
import numpy as np

# 📌 Load CSV Data
def load_plant_data():
    try:
        data = pd.read_csv('plants.csv', encoding="ISO-8859-1")
        data.columns = data.columns.str.strip()  
        data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()
import pandas as pd

effect_scores = {
    "Strong Inhibition": -2,
    "Weakened Inhibition": -1,
    "No Effect": 0,
    "Weakened Exhibition": 1,
    "Strong Exhibition": 2
}

def get_recommendations(plant_data, selected_plant):
    """Find companion plants and plants to avoid based on aggregated chemical interactions."""
    plant_chemicals = plant_data[plant_data["Source Plant"] == selected_plant]

    if plant_chemicals.empty or "Target Plants" not in plant_chemicals.columns or "Effect" not in plant_chemicals.columns:
        return [], []

    # ✅ Convert Effects to Scores
    plant_chemicals["Effect Score"] = plant_chemicals["Effect"].map(effect_scores)

    # ✅ Aggregate Effects per Target Plant
    aggregated_effects = (
        plant_chemicals.groupby("Target Plants")["Effect Score"]
        .sum()
        .reset_index()
    )

    # ✅ Classify as Companion or Suppressor
    companion_plants = aggregated_effects[aggregated_effects["Effect Score"] >= 0]["Target Plants"].tolist()
    suppressor_plants = aggregated_effects[aggregated_effects["Effect Score"] < 0]["Target Plants"].tolist()

    return companion_plants, suppressor_plants


# 📌 Show Plant Info
def show():
    st.header("🌿 Allelopathic Plant Insights")

    # ✅ Load Data
    plant_data = load_plant_data()

    # ✅ Ensure Data is Loaded
    if plant_data.empty or "Source Plant" not in plant_data.columns or "Main Allelochemical" not in plant_data.columns:
        st.error("⚠️ Plant data could not be loaded correctly. Please check the CSV file format.")
        return

    # ✅ Plant Selection
    all_plants = sorted(plant_data["Source Plant"].dropna().unique().tolist())
    selected_plant = st.selectbox("Select a plant to view its chemical profile:", all_plants)

    if selected_plant:
        st.subheader(f"🌱 {selected_plant} - Chemical Profile")
        plant_chemicals = plant_data[plant_data["Source Plant"] == selected_plant]

        if not plant_chemicals.empty:
            chemicals = plant_chemicals["Main Allelochemical"].dropna().unique().tolist()

            if chemicals:
                st.write(f"**Main Allelochemicals:** {', '.join(chemicals)}")
                chem_tabs = st.tabs(chemicals)

                for i, chem in enumerate(chemicals):
                    with chem_tabs[i]:
                        st.write(f"### 🔬 {chem} Interactions")
                        chem_data = plant_chemicals[plant_chemicals["Main Allelochemical"] == chem]

                        if "Target Plants" in chem_data.columns and "Effect" in chem_data.columns:
                            interaction_data = chem_data[["Target Plants", "Effect"]]
                            interaction_data.index = np.arange(1, len(interaction_data) + 1)
                            interaction_data.index.name = "S. No."
                            st.write("#### 🌿 Target Plant Interactions")
                            st.dataframe(interaction_data, use_container_width=True)

            else:
                st.warning(f"No allelochemicals found for {selected_plant}.")

            # ✅ Aggregate Effect-Based Recommendations
            st.subheader("📌 Recommendations Based on Aggregate Effects")
            companion_plants, suppressor_plants = get_recommendations(plant_data, selected_plant)

            # ✅ Display Companion Plants
            if companion_plants:
                st.success("🌿 **Recommended Companion Plants:**")
                st.write(", ".join(companion_plants))

            # ✅ Display Suppressed Plants
            if suppressor_plants:
                st.error("⚠️ **Avoid Planting With:**")
                st.write(", ".join(suppressor_plants))

        else:
            st.info(f"No data available for {selected_plant}. Please select another plant.")
