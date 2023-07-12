import streamlit as st
from streamlit_option_menu import option_menu
from st_pages import Page, show_pages, add_page_title
from streamlit_folium import folium_static, st_folium
import folium
import pandas as pd

#Display all rows
pd.set_option('display.max_rows', 500)

pd.set_option('display.max_columns', None)

#Streamlit
st.set_page_config(page_title="WG Gesucht Analysis", layout="wide", initial_sidebar_state="expanded", menu_items={
    'Get Help': 'https://www.extremelycoolapp.com/help',
    'Report a bug': "https://www.extremelycoolapp.com/bug",
    'About': "# This is a header. This is an *extremely* cool app!"
})
st.markdown("<h1 style='text-align: center; color: orange;'>Property Analysis</h1>", unsafe_allow_html=True)

#Pages
page_real_estate_general_dashboard = "wggesucht.py"
page_maps = "pages/maps.py"
#page_payments = "/Users/christianheins/Documents/Coding/Projects/WGGesucht/pages/wggesucht3.py"

show_pages(
    [
        Page(page_real_estate_general_dashboard, "General Dashboard", "🏠"),
        Page(page_maps, "Maps", "🗺️"),
    ]
)

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stHeader"] {
                background-image: url(https://www.lautgegennazis.de/wp-content/uploads/2016/10/WG_Banner.jpg);
                background-repeat: no-repeat;
                background-position: 62%;
                background-size: contain;
                padding-top: 100px;
            }
            [data-testid="stSidebarNav"] {
                background-image: url(https://raw.githubusercontent.com/christianheins/wggesucht/main/images/4.jpg);
                background-repeat: no-repeat;
                background-size: contain;
                background-position: 50% 0%;
                padding-top: 80px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "Pages";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
add_logo()

st.sidebar.header("Sections")

st.sidebar.text("Hi!")

st.markdown("<h3 style='text-align: center; color: orange;'>Mapssss 🦮</h3>", unsafe_allow_html=True)

nameofdataframe = r"df_concat_20230422.csv"
filename_csv_table_realestate_from_reporting = nameofdataframe
df_map = pd.read_csv(filename_csv_table_realestate_from_reporting)
df_map.fillna(0, inplace=True)
latitudes = ["Location not found: Wedding","Location not found: Reinickendorf","Location not found: Prenzlauer Berg","Location not found: Neukölln","Location not found: NA","Location not found: Moabit","Location not found: Mitte","Location not found: Marienfelde","Location not found: Lichtenberg","Location not found: Kreuzberg","Location not found: Charlottenburg"]
df_map = df_map[~df_map["Latitude"].isin(latitudes)]
df_map["Latitude"] = df_map["Latitude"].astype(float)
df_map["Longitude"] = df_map["Longitude"].astype(float)
#df_map = df_map[["Latitude","Longitude","Country","Property Status", "Property"]]
df_map.rename(columns = {"Latitude":"lat","Longitude":"lon"}, inplace = True)
st.write(df_map)
col1, col2 = st.columns([0.5, 1.5])

with col1:
    st.markdown("<h3 style='text-align: center; color: red;'>Filters 🎛️</h3>", unsafe_allow_html=True)
    subsidiary = st.multiselect("Please choose a Country", options=df_map["Neighbourhood"].unique(), help="Please do not leave empty")
    #df_filteredbysubsidiary = df_sheet_bills_sorted[df_sheet_bills_sorted["Subsidiary (no hierarchy)"] == subsidiary[0]]
    df_filteredbysubsidiary = df_map[df_map["Neighbourhood"].isin(subsidiary)]
    warehouse = st.multiselect("Please choose a property", options=df_filteredbysubsidiary["Name"].unique(), help="Please do not leave empty")
    st.write("Selection:")
    st.write(warehouse)
    if subsidiary == []:
        df_map = df_map
    elif warehouse == []:
        df_map = df_filteredbysubsidiary
    else:
        df_map = df_map[df_map["Name"].isin(warehouse)]

    st.metric("Current Pure Rent:", df_map["Miete"].reset_index(drop=True)[0])
    st.write(df_map["Neighbourhood"].reset_index(drop=True))


with col2:
    st.markdown("<h3 style='text-align: center; color: red;'>Location 📍</h3>", unsafe_allow_html=True)
    st.markdown("<a href='https://www.appsheet.com/start/135c691c-2e06-418d-a0df-f206a7e51f3d?platform=desktop#viewStack[0][identifier][Type]=Control&viewStack[0][identifier][Name]=Map&appName=00_Existingdarkstores-4626010-22-09-06'>Link to google maps</a>", unsafe_allow_html=True)
    df_map.reset_index(inplace=True)
    if len(df_map) == 1:
        map = folium.Map(location=[float(df_map["lat"][0]), float(df_map["lon"][0])], zoom_start=16)
    else:
        map = folium.Map(location=[float(df_map["lat"][0]), float(df_map["lon"][0])], zoom_start=7)

    #df_map.apply(lambda row:folium.Marker(location=[row["lat"], row["lon"]], popup=row.loc["Property"], tooltip=row.loc["Property"]).add_to(map), axis=1)

    for (index, row) in df_map.iterrows():
        folium.Marker(location=[row["lat"], row["lon"]], tooltip=row["Name"], popup="example").add_to(map)

    bordersStyle = {
        'color':'red',
        'weight': 2,
        'fillColor':'blue',
        'fillOpacity': 0.3
    }
    # Opening JSON file
    #f = open('/Users/christianheins/Desktop/Pythontools/Reports/ELT_Report/pages/RE BULLSEYES 28_04.geojson')

    # returns JSON object as
    # a dictionary
    #data = json.load(f)

    #f2 = open('/Users/christianheins/Desktop/Pythontools/Reports/ELT_Report/pages/RE BULLSEYES 28_042.geojson', 'r')

    # returns JSON object as
    # a dictionary
    #data2 = json.load(f2)

    #folium.GeoJson(data, name="Polygons 2").add_to(map)
    #folium.GeoJson(data2, name="Polygons").add_to(map)
    st_map = st_folium(map, width=1500, height=800)
    map.save("output.html")
    print("File created")
    st.markdown("""
        <style>
        .StMarkdown {
            height: 500px;
            width: 800px;
            border-radius: 20px;
            border: 2px solid #008080;
            box-shadow: 5px 5px 10px #888888;
        }
        </style>
    """, unsafe_allow_html=True)
    #st.json(data)
#folium.Marker(location=[dfmap["lat"], warehouserow["lon"]],tooltip=row["Property"], popup="example").add_to(map)
#st_map = st_folium(map, width=1500, height=800)


