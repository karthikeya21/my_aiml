import streamlit as st
import pandas as pd
import numpy as np

def load_chemical_data():
    try:
        data = pd.read_csv('chemicals.csv',encoding="ISO-8859-1")
        data.columns = data.columns.str.strip()  # Remove extra spaces from column names
        data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if loading fails

def show():
    st.header("🧪 Chemical Group Information")

    # ✅ Load Data
    chemical_data = load_chemical_data()

    # ✅ Ensure Data is Loaded
    if "Main Allelochemical" not in chemical_data.columns:
        st.error("⚠️ Chemical group data could not be loaded correctly. Please check the CSV file format.")
        return
    unique_groups = sorted(chemical_data['Group'].dropna().unique().tolist())
    selected_group = st.selectbox("Select a chemical group to view its plants profile:", unique_groups)
    if selected_group:
        st.subheader(f"🌱 {selected_group} - Chemicals")

        # ✅ Filter Data for the Selected group
        chemicals = chemical_data[chemical_data["Group"] == selected_group]
        if not chemicals.empty:
            # ✅ Extract & Display Unique Chemicals
            chemicals_list = chemicals["Main Allelochemical"].dropna().unique().tolist()

            if chemicals_list:
                st.write(f"**Main Allelochemicals:** {', '.join(chemicals_list)}")

                # ✅ Create Tabs for Each Chemical
                chem_tabs = st.tabs(chemicals_list)

                for i, chem in enumerate(chemicals_list):
                    with chem_tabs[i]:
                        st.write(f"### 🔬 {chem} Interactions")

                        # ✅ Filter Data for the Specific Chemical
                        chem_data = chemicals[chemicals["Main Allelochemical"] == chem]

                        if "Source Plant" in chem_data.columns and "Target Plants" in chem_data.columns and "Effect" in chem_data.columns:
                            interaction_data = chem_data[["Source Plant","Target Plants", "Effect"]]
                            interaction_data.index = np.arange(1, len(interaction_data) + 1)
                            interaction_data.index.name = "S. No."
                            st.write("#### 🌿 Source Plant - Target Plant Interactions")
                            st.dataframe(interaction_data, use_container_width=True)

                            # ✅ Show Summary Metrics
                            strong_inhibit = (interaction_data["Effect"] == "Strong Inhibition").sum()
                            weak_inhibit = (interaction_data["Effect"] == "Weakened Inhibition").sum()
                            strong_exhibit = (interaction_data["Effect"]== "Strong Exhibition").sum()
                            weak_exhibit = (interaction_data["Effect"]== "Weakened Exhibition").sum()
                            no_effect = (interaction_data["Effect"] == "No Effect").sum()

                            col1, col2, col3,col4,col5 = st.columns(5)
                            col1.metric("🔥 Strong Inhibition", strong_inhibit)
                            col2.metric("⚠️ Weakened Inhibition", weak_inhibit)
                            col3.metric("✅ No Effect", no_effect)
                            col4.metric("🚀 Strong Exhibition", strong_exhibit)  
                            col5.metric("🌸 Weakened Exhibition", weak_exhibit) 

                        else:
                            st.warning("⚠️ Data missing for Target Plant interactions.")
            else:
                st.warning(f"No allelochemicals found for {selected_group}.")
        else:
            st.info(f"No data available for {selected_group}. Please select another plant.")


