import streamlit as st
import prediction_module
import plant_info_provider
import chemical_info_provider

# Set page configuration
st.set_page_config(
    page_title="Allelopathic Influence Prediction & Insights",
    page_icon="🪴",
    layout="wide"
)

def main():
    # Main application title
    st.title("🪴 Allelopathic Influence Prediction & Insights")
    
    # Create sidebar for module selection
    st.sidebar.title("Module Selection")
    module_option = st.sidebar.radio(
        "Choose a module to use:",
        ["🌿 Allelopathy Effect Predictor","🌱 Plant Profile & Chemical Interactions","⚗️ Allelochemical Group Insights"]
    )
    
    # Load the selected module
    if module_option == "🌿 Allelopathy Effect Predictor":
        prediction_module.show()
    elif module_option == "🌱 Plant Profile & Chemical Interactions":
         plant_info_provider.show()
    elif module_option == "⚗️ Allelochemical Group Insights":
         chemical_info_provider.show()

if __name__ == "__main__":
    main()