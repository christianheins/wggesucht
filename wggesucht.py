def main():
    import requests
    import pandas as pd
    import streamlit as st
    from streamlit_option_menu import option_menu
    from st_pages import Page, show_pages, add_page_title
    import numpy as np
    import altair as alt
    import urllib.parse

    pd.set_option('display.max_columns', None)

    #Streamlit
    st.set_page_config(page_title="WG Gesucht Analysis", layout="wide")
    st.markdown("<h1 style='text-align: center; color: orange;'>Property Analysis</h1>", unsafe_allow_html=True)

    #Pages
    page_real_estate_general_dashboard = "wggesucht.py"
    page_maps = "/pages/wggesucht2.py"
    page_payments = "/Users/christianheins/Documents/Coding/Projects/WGGesucht/pages/wggesucht3.py"

    show_pages(
        [
            Page(page_real_estate_general_dashboard, "General Dashboard", "🏠"),
            Page(page_maps, "Maps", "🏠"),
        ]
    )

    with st.sidebar:
        st.sidebar.header("Sections")
        selected = option_menu(
            menu_title="Finance Menu",
            options=["🏘️ Apartments", "🫂 Neighbourhoods"], #https://icons.getbootstrap.com/
            orientation="vertical",
        )

        button_pressed = False
        st.markdown("""---""")
        st.markdown("<p style='text-align: center; color: red;'>Click to refresh the WGGesucht dataframe</p>", unsafe_allow_html=True)
        if st.button("Refresh", use_container_width=True):
            button_pressed = True
            st.write("Button pressed!")

            def requestswg():

                '''
                url = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"

                # Add headers to mimic a browser request
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }

                response = requests.get(url, headers=headers)

                # check the status code of the response
                print(response.status_code)

                # access the content of the response
                html_content = response.content
                print(html_content)
                '''

                #url = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"
                url = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html?offer_filter=1&city_id=8&sort_order=0&noDeact=1&categories%5B%5D=1&categories%5B%5D=2&rent_types%5B%5D=0#back_to_ad_9597345"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }
                response = requests.get(url, headers=headers)
                print(response)

                dfs = pd.read_html(response.content)
                df = dfs[0]  # assuming the desired table is the first one on the page
                #for df in dfs:
                #    print(df)

                # Format the dataframe
                df['frei bis'] = pd.to_datetime(df['frei bis'], dayfirst=True)
                df['frei ab'] = pd.to_datetime(df['frei ab'], dayfirst=True)
                df["Größe"] = df['Größe'].str.replace("m²","")
                df["Miete"] = df['Miete'].str.replace(" €","")
                df["Miete"] = df['Miete'].str.replace("€","")
                df[["Miete", "Größe"]] = df[["Miete", "Größe"]].astype(float)
                df["Lease term"] = df["frei bis"] - df["frei ab"]
                #print(df.columns)
                #print(df["Lease term"])

                # Create two date objects
                date1 = pd.to_datetime('2022-03-20')
                date2 = pd.to_datetime('2022-03-25')

                # Calculate the difference between the two dates
                diff = date2 - date1

                # Print the difference in days

                #print(diff.days)


                df['Lease term'] = (df['frei bis'].dt.year - df['frei ab'].dt.year) * 12 + (df['frei bis'].dt.month - df['frei ab'].dt.month)

                df["EUR / SQM"] = df["Miete"] / df["Größe"]
                #print(df)
                return df

            def requestswg2():

                '''
                url = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"

                # Add headers to mimic a browser request
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }

                response = requests.get(url, headers=headers)

                # check the status code of the response
                print(response.status_code)

                # access the content of the response
                html_content = response.content
                print(html_content)
                '''

                #url1 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"
                url2 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.1.html?pagination=1&pu="
                url3 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.2.html?pagination=1&pu="
                url4 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.3.html?pagination=1&pu="

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }
                response = requests.get(url2, headers=headers)

                dfs = pd.read_html(response.content)
                df = dfs[0]  # assuming the desired table is the first one on the page

                # Format the dataframe
                df['frei bis'] = pd.to_datetime(df['frei bis'], dayfirst=True)
                df['frei ab'] = pd.to_datetime(df['frei ab'], dayfirst=True)
                df["Größe"] = df['Größe'].str.replace("m²","")
                df["Miete"] = df['Miete'].str.replace(" €","")
                df["Miete"] = df['Miete'].str.replace("€","")
                df[["Miete", "Größe"]] = df[["Miete", "Größe"]].astype(float)
                df["Lease term"] = df["frei bis"] - df["frei ab"]
                #print(df.columns)
                #print(df["Lease term"])

                # Create two date objects
                date1 = pd.to_datetime('2022-03-20')
                date2 = pd.to_datetime('2022-03-25')

                # Calculate the difference between the two dates
                diff = date2 - date1

                # Print the difference in days

                #print(diff.days)


                df['Lease term'] = (df['frei bis'].dt.year - df['frei ab'].dt.year) * 12 + (df['frei bis'].dt.month - df['frei ab'].dt.month)

                df["EUR / SQM"] = df["Miete"] / df["Größe"]
                #print(df)
                return df

            def requestswg3():

                '''
                url = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"

                # Add headers to mimic a browser request
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }

                response = requests.get(url, headers=headers)

                # check the status code of the response
                print(response.status_code)

                # access the content of the response
                html_content = response.content
                print(html_content)
                '''

                #url1 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"
                url2 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.1.html?pagination=1&pu="
                url3 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.2.html?pagination=1&pu="
                url4 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.3.html?pagination=1&pu="

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }
                response = requests.get(url3, headers=headers)

                dfs = pd.read_html(response.content)
                df = dfs[0]  # assuming the desired table is the first one on the page

                # Format the dataframe
                df['frei bis'] = pd.to_datetime(df['frei bis'], dayfirst=True)
                df['frei ab'] = pd.to_datetime(df['frei ab'], dayfirst=True)
                df["Größe"] = df['Größe'].str.replace("m²","")
                df["Miete"] = df['Miete'].str.replace(" €","")
                df["Miete"] = df['Miete'].str.replace("€","")
                df[["Miete", "Größe"]] = df[["Miete", "Größe"]].astype(float)
                df["Lease term"] = df["frei bis"] - df["frei ab"]
                #print(df.columns)
                #print(df["Lease term"])

                # Create two date objects
                date1 = pd.to_datetime('2022-03-20')
                date2 = pd.to_datetime('2022-03-25')

                # Calculate the difference between the two dates
                diff = date2 - date1

                # Print the difference in days

                #print(diff.days)


                df['Lease term'] = (df['frei bis'].dt.year - df['frei ab'].dt.year) * 12 + (df['frei bis'].dt.month - df['frei ab'].dt.month)

                df["EUR / SQM"] = df["Miete"] / df["Größe"]
                #print(df)
                return df

            def requestswg4():

                '''
                url = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"

                # Add headers to mimic a browser request
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }

                response = requests.get(url, headers=headers)

                # check the status code of the response
                print(response.status_code)

                # access the content of the response
                html_content = response.content
                print(html_content)
                '''

                #url1 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"
                url2 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.1.html?pagination=1&pu="
                url3 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.2.html?pagination=1&pu="
                url4 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.3.html?pagination=1&pu="

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }
                response = requests.get(url4, headers=headers)

                dfs = pd.read_html(response.content)
                df = dfs[0]  # assuming the desired table is the first one on the page

                # Format the dataframe
                df['frei bis'] = pd.to_datetime(df['frei bis'], dayfirst=True)
                df['frei ab'] = pd.to_datetime(df['frei ab'], dayfirst=True)
                df["Größe"] = df['Größe'].str.replace("m²","")
                df["Miete"] = df['Miete'].str.replace(" €","")
                df["Miete"] = df['Miete'].str.replace("€","")
                df[["Miete", "Größe"]] = df[["Miete", "Größe"]].astype(float)
                df["Lease term"] = df["frei bis"] - df["frei ab"]
                #print(df.columns)
                #print(df["Lease term"])

                # Create two date objects
                date1 = pd.to_datetime('2022-03-20')
                date2 = pd.to_datetime('2022-03-25')

                # Calculate the difference between the two dates
                diff = date2 - date1

                # Print the difference in days
                #print(diff.days)


                df['Lease term'] = (df['frei bis'].dt.year - df['frei ab'].dt.year) * 12 + (df['frei bis'].dt.month - df['frei ab'].dt.month)

                df["EUR / SQM"] = df["Miete"] / df["Größe"]
                #print(df)
                return df

            def requestswg5():

                '''
                url = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"

                # Add headers to mimic a browser request
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }

                response = requests.get(url, headers=headers)

                # check the status code of the response
                print(response.status_code)

                # access the content of the response
                html_content = response.content
                print(html_content)
                '''

                url1 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"
                url2 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.1.html?pagination=1&pu="
                url3 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.2.html?pagination=1&pu="
                url4 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.3.html?pagination=1&pu="
                url5 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.4.html?pagination=1&pu="


                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }
                response = requests.get(url5, headers=headers)

                dfs = pd.read_html(response.content)
                df = dfs[0]  # assuming the desired table is the first one on the page

                # Format the dataframe
                df['frei bis'] = pd.to_datetime(df['frei bis'], dayfirst=True)
                df['frei ab'] = pd.to_datetime(df['frei ab'], dayfirst=True)
                df["Größe"] = df['Größe'].str.replace("m²","")
                df["Miete"] = df['Miete'].str.replace(" €","")
                df["Miete"] = df['Miete'].str.replace("€","")
                df[["Miete", "Größe"]] = df[["Miete", "Größe"]].astype(float)
                df["Lease term"] = df["frei bis"] - df["frei ab"]
                #print(df.columns)
                #print(df["Lease term"])

                # Create two date objects
                date1 = pd.to_datetime('2022-03-20')
                date2 = pd.to_datetime('2022-03-25')

                # Calculate the difference between the two dates
                diff = date2 - date1

                # Print the difference in days
                #print(diff.days)


                df['Lease term'] = (df['frei bis'].dt.year - df['frei ab'].dt.year) * 12 + (df['frei bis'].dt.month - df['frei ab'].dt.month)

                df["EUR / SQM"] = df["Miete"] / df["Größe"]
                #print(df)
                return df

            df1 = requestswg()
            df2 = requestswg2()
            df3 = requestswg3()
            df4 = requestswg4()
            df5 = requestswg5()

            df_concat = pd.concat([df1, df2, df3, df4, df5])
            df_concat.reset_index(drop=True, inplace=True)

            #Cleaning out the neighbourhoods

            neighbourhoods = df_concat["Stadtteil"].unique()
            df_concat["Neighbourhood"] = ""

            neighbourhoods_list = ["Blankenburg", "Charlottenburg", "Friedrichshain", "Kreuzberg", "Mitte", "Moabit", "Neukölln", "Prenzlauer Berg"]
            neighbourhoods_clean = []
            neighbourhoods_dirty = df_concat["Stadtteil"].to_numpy().tolist()
            print(neighbourhoods_dirty)

            '''
            for neighbourhood in neighbourhoods_list:
                for neighbourhood_dirty in neighbourhoods_dirty:
                    if str(neighbourhood_dirty).__contains__(f"{neighbourhood}"):
                        neighbourhoods_clean.append(f"{neighbourhood}")
                    else:
                        neighbourhoods_clean.append("NA")
            print(neighbourhoods_clean)
            '''

            for neighbourhood in neighbourhoods_dirty:
                print(str(neighbourhood))

                if str(neighbourhood).__contains__("Alt- Treptower"):
                    print("Alt- Treptower")
                    neighbourhoods_clean.append("Blankenburg")

                elif str(neighbourhood).__contains__("Blankenburg"):
                    print("Blankenburg")
                    neighbourhoods_clean.append("Blankenburg")

                elif str(neighbourhood).__contains__("Charlottenburg"):
                    print("Charlottenburg")
                    neighbourhoods_clean.append("Charlottenburg")

                elif str(neighbourhood).__contains__("Friedrichshain"):
                    print("Kreuzberg")
                    neighbourhoods_clean.append("Friedrichshain")

                elif str(neighbourhood).__contains__("Hermsdorf"):
                    print("Hermsdorf")
                    neighbourhoods_clean.append("Hermsdorf")

                elif str(neighbourhood).__contains__("Kreuzberg"):
                    print("Kreuzberg")
                    neighbourhoods_clean.append("Kreuzberg")

                elif str(neighbourhood).__contains__("Lichtenberg"):
                    print("Lichtenberg")
                    neighbourhoods_clean.append("Lichtenberg")

                elif str(neighbourhood).__contains__("Marienfelde"):
                    print("Mitte")
                    neighbourhoods_clean.append("Marienfelde")

                elif str(neighbourhood).__contains__("Mitte"):
                    print("Mitte")
                    neighbourhoods_clean.append("Mitte")

                elif str(neighbourhood).__contains__("Moabit"):
                    print("Moabit")
                    neighbourhoods_clean.append("Moabit")

                elif str(neighbourhood).__contains__("Neukölln"):
                    print("Neukölln")
                    neighbourhoods_clean.append("Neukölln")

                elif str(neighbourhood).__contains__("Prenzlauer Berg"):
                    print("Prenzlauer Berg")
                    neighbourhoods_clean.append("Prenzlauer Berg")

                elif str(neighbourhood).__contains__("Tempelhof"):
                    print("Tempelhof")
                    neighbourhoods_clean.append("Tempelhof")

                elif str(neighbourhood).__contains__("Wedding"):
                    print("Wedding")
                    neighbourhoods_clean.append("Wedding")

                elif str(neighbourhood).__contains__("Weißensee"):
                    print("Weißensee")
                    neighbourhoods_clean.append("Weißensee")

                elif str(neighbourhood).__contains__("Wilmersdorf"):
                    print("Wedding")
                    neighbourhoods_clean.append("Wedding")

                else:
                    neighbourhoods_clean.append(("NA"))


            df_concat["Neighbourhood"] = neighbourhoods_clean
            df_concat['frei bis (Year - Month)'] = pd.to_datetime(df_concat['frei bis']).dt.to_period('M')
            print(neighbourhoods_clean)

            addresses = df_concat["Neighbourhood"].to_list()
            print(len(addresses))

            latitudes = []
            longitudes = []

            for location in addresses:
                try:
                    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(location) +'?format=json'
                    response = requests.get(url).json()
                    print("Address: "+location)
                    print("latitude: "+response[0]["lat"])
                    print("longitude: "+response[0]["lon"])
                    latitudes.append(response[0]["lat"])
                    longitudes.append(response[0]["lon"])
                    print("Next...")
                except:
                    latitudes.append("Location not found: "+location)
                    longitudes.append("Location not found: "+location)
                    print("Location not found: "+location)

            df_concat["Latitude"] = latitudes
            df_concat["Longitude"] = longitudes

            nameofdataframe ="df_concat.csv"
            df_concat.to_csv(f"{nameofdataframe}")
            st.write(f"Dataframe with name {nameofdataframe} created.")
            button_pressed = False

            if button_pressed:
                st.write("Processing...")
            else:
                st.write("Ready to refresh again!")



    df_concat = pd.read_csv("df_concat.csv")

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
                    background-image: url(https://play-lh.googleusercontent.com/FMudTGzgSiUN0ebC3gG5WkSBGn_xGA3M5FDs73F6G8Eam_pLhckoTbO53tMalltHKxw);
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


    if selected == "🏘️ Apartments":

        col1, col2, col3 = st.columns([0.2, 0.2, 0.6])
        with col1:
            st.metric("Available apartments", value="{:,.0f}".format(len(df_concat)))
        with col2:
            st.metric("Unique neighbourhoods", value="{:,.0f}".format(len(df_concat[['Rubrik', 'Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood']].pivot_table(index="Neighbourhood", values="Eintrag", aggfunc="count").reset_index())))
        with col3:
            st.markdown("<h6 style='text-align: left; color: red;'>Instructions</h6>", unsafe_allow_html=True)
            st.markdown(f"<li style='text-align: left; color: grey; font-size: 12px;'>This web applications is capturing a snapshot of the last 3 months entries as of the date the csv file was lastly refreshed</li>", unsafe_allow_html=True)
            st.markdown(f"<li style='text-align: left; color: grey; font-size: 12px;'>Please use as a guide for only the WG Gesucht portal, this data is not completly representative.</li>", unsafe_allow_html=True)
        st.markdown("""---""")

        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            #st.metric("Min rent", value="{:,.0f} €".format(df_concat["Miete"].min()))
            st.metric("Average rent", value="{:,.0f} €".format(df_concat["Miete"].mean()))
            st.metric("Max rent", value="{:,.0f} €".format(df_concat["Miete"].max()))
        with col2:
            #st.metric("Min size", value="{:,.0f} SQM".format(df_concat["Größe"].min()))
            st.metric("Average size", value="{:,.0f} SQM".format(df_concat["Größe"].mean()))
            st.metric("Max size", value="{:,.0f} SQM".format(df_concat["Größe"].max()))
        with col3:
            #st.metric("Min EUR per SQM", value="{:,.0f} € per SQM".format(df_concat["EUR / SQM"].min()))
            st.metric("Average EUR per SQM", value="{:,.0f} € per SQM".format(df_concat["EUR / SQM"].mean()))
            st.metric("Max EUR per SQM", value="{:,.0f} € per SQM".format(df_concat["EUR / SQM"].max()))
        with col4:
            #st.metric("Min lease term", value="{:,.0f} months".format(df_concat["Lease term"].min()))
            st.metric("Average lease term", value="{:,.0f} months".format(df_concat["Lease term"].mean()))
            st.metric("Longest lease term", value="{:,.0f} months".format(df_concat["Lease term"].max()))

        st.markdown("""---""")
        df_concat_neighbourhoods = df_concat[['Rubrik', 'Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood']].pivot_table(index="Neighbourhood", values="Eintrag", aggfunc="count").reset_index()
        df_concat_neighbourhoods.sort_values(by=["Eintrag"], ascending=[False], inplace=True)

        df_concat_endofleaseterm = df_concat[['Rubrik', 'Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood', 'Lease term']].pivot_table(index="Lease term", values="Eintrag", aggfunc="count").reset_index()
        df_concat_endofleaseterm.sort_values(by=["Eintrag"], ascending=[True], inplace=True)


        col1, col2 = st.columns([0.6, 0.4])
        with col1:
            st.markdown("<h6 style='text-align: center; color: orange;'>Properties table</h6>", unsafe_allow_html=True)
            st.write(df_concat[['Rubrik', 'Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood', 'frei ab', 'frei bis','frei bis (Year - Month)', 'Lease term', 'Latitude', 'Longitude']])

        with col2:
            st.markdown("<h6 style='text-align: center; color: orange;'>Neighbourghoods</h6>", unsafe_allow_html=True)
            chart = alt.Chart(df_concat_neighbourhoods).encode(
                x=alt.X('Eintrag:Q'),
                y=alt.Y('Neighbourhood:N', sort=None), #use 'sort=None' to preserve the order of categories
                text=alt.Text('Eintrag', format='.1f')
            )
            #Combine bar chart with text chart, weird isnt?

            #wholechart = chart.mark_bar(color="orange") + chart.mark_text(align='left', dx=8, color="black")

            wholechart = alt.layer(chart.mark_bar(color="orange"), chart.mark_text(align='left', dx=8, color="black"))

            st.altair_chart(wholechart.interactive(), use_container_width=True)

        col1, col2, col3 = st.columns([0.4, 0.2, 0.4])

        with col1:
            st.markdown("<h6 style='text-align: center; color: orange;'>Numerical values described</h6>", unsafe_allow_html=True)

            st.write(df_concat[["Miete", "Größe", 'EUR / SQM', "Lease term"]].describe())
        with col2:
            st.markdown("<h6 style='text-align: center; color: orange;'>Lease term exact count</h6>", unsafe_allow_html=True)
            st.write(df_concat_endofleaseterm)
        with col3:
            st.markdown("<h6 style='text-align: center; color: orange;'>Lease term Chart</h6>", unsafe_allow_html=True)
            chart = alt.Chart(df_concat_endofleaseterm).encode(
                x=alt.X('Lease term:Q'),
                y=alt.Y('Eintrag:Q', sort=None), #use 'sort=None' to preserve the order of categories
                text=alt.Text('Eintrag', format='.1f')
            )
            #Combine bar chart with text chart, weird isnt?
            wholechart = alt.layer(chart.mark_bar(color="orange"), chart.mark_text(align='center', dy=-5, color="black"))

            st.altair_chart(wholechart.interactive(), use_container_width=True)

        st.markdown("""---""")
        st.markdown("<h3 style='text-align: center; color: orange;'>Map</h6>", unsafe_allow_html=True)

        df_concat.rename(columns = {"Latitude":"lat","Longitude":"lon"}, inplace=True)

        st.map(df_concat)

        with st.container():
            st.write("This is inside the container")

            # You can call any Streamlit command, including custom components:
            st.bar_chart(np.random.randn(50, 3))

        st.write("This is outside the container")

    if selected == "🏘️ Neighbourhoods":
        st.write("Hello")

if __name__ == "__main__":
    main()