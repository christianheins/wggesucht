def main():
    import requests
    import pandas as pd
    import streamlit as st
    from streamlit_option_menu import option_menu
    from st_pages import Page, show_pages, add_page_title
    import numpy as np
    import altair as alt
    import urllib.parse
    import os
    import datetime as dt
    import base64
    from github import Github
    from github import InputFileContent

    #Streamlit
    #Pages
    page_real_estate_general_dashboard = "wggesucht.py"
    page_maps = "pages/maps.py"

    show_pages(
        [
            Page(page_real_estate_general_dashboard, "General Dashboard", "🏠"),
            Page(page_maps, "Maps", "🗺️"),
        ]
    )

    st.set_page_config(page_title="WG Gesucht Analysis", layout="wide", initial_sidebar_state="expanded", menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

    pd.set_option('display.max_columns', None)

    nameofdataframe = "df_concat.csv"

    with st.sidebar:
        st.sidebar.header("Sections")
        selected = option_menu(
            menu_title="Menu",
            options=["🏘️ Apartments", "🫂 Neighbourhoods", "📑 Sample contracts"], #https://icons.getbootstrap.com/
            orientation="vertical",
        )

        #Create a button
        button_pressed = False
        st.markdown("""---""")
        st.markdown("<p style='text-align: center; color: red;'>Click to refresh the WG-Gesucht dataframe</p>", unsafe_allow_html=True)
        if st.button("Refresh", use_container_width=True):
            button_pressed = True
            st.write("Button pressed!")

            def requestswg_all():

                df_toupdate = []
                for i in range(0,50):

                    url = f"https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.{i}.html?pagination=1&pu="
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
                    df_toupdate.append(df)

                df = pd.concat(df_toupdate)
                return df

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

            #df1 = requestswg()
            #df2 = requestswg2()
            #df3 = requestswg3()
            #df4 = requestswg4()
            #df5 = requestswg5()

            #df_concat = pd.concat([df1, df2, df3, df4, df5])
            df_concat = requestswg_all()
            df_concat.dropna(subset=["Eintrag"], inplace=True)
            df_concat.reset_index(drop=True, inplace=True)

            #Give eachrow a name
            def combine_names(row):
                return str(row['Eintrag']) + '-' + str(row['Miete'])  + '-' + str(row['EUR / SQM']) + ' ' + str(row['Stadtteil'])

            df_concat['Name'] = df_concat.apply(combine_names, axis=1)

            #Cleaning out the neighbourhoods
            neighbourhoods = df_concat["Stadtteil"].unique()
            df_concat["Neighbourhood"] = ""

            neighbourhoods_list = ["Blankenburg", "Charlottenburg", "Friedrichshain", "Kreuzberg", "Mitte", "Moabit", "Neukölln", "Prenzlauer Berg"]
            neighbourhoods_clean = []
            neighbourhoods_dirty = df_concat["Stadtteil"].to_numpy().tolist()
            print(neighbourhoods_dirty)

            #Clean out neighbourhoods
            for neighbourhood in neighbourhoods_dirty:
                print(str(neighbourhood))

                if str(neighbourhood).__contains__("Altglienicke"):
                    print("Altglienicke")
                    neighbourhoods_clean.append("Altglienicke")

                elif str(neighbourhood).__contains__("Alt- Treptower"):
                    print("Alt- Treptower")
                    neighbourhoods_clean.append("Alt-Treptow")

                elif str(neighbourhood).__contains__("Blankenburg"):
                    print("Blankenburg")
                    neighbourhoods_clean.append("Blankenburg")

                elif str(neighbourhood).__contains__("Buch"):
                    print("Buch")
                    neighbourhoods_clean.append("Buch")

                elif str(neighbourhood).__contains__("Charlottenburg"):
                    print("Charlottenburg")
                    neighbourhoods_clean.append("Charlottenburg")

                elif str(neighbourhood).__contains__("Friedrichshain"):
                    print("Friedrichshain")
                    neighbourhoods_clean.append("Friedrichshain")

                elif str(neighbourhood).__contains__("Friedrischain"):
                    print("Friedrischain")
                    neighbourhoods_clean.append("Friedrichshain")

                elif str(neighbourhood).__contains__("Gesundbrunnen"):
                    print("Gesundbrunnen")
                    neighbourhoods_clean.append("Gesundbrunnen")

                elif str(neighbourhood).__contains__("Halensee"):
                    print("Halensee")
                    neighbourhoods_clean.append("Halensee")

                elif str(neighbourhood).__contains__("Hellersdorf"):
                    print("Hellersdorf")
                    neighbourhoods_clean.append("Hellersdorf")

                elif str(neighbourhood).__contains__("Hermsdorf"):
                    print("Hermsdorf")
                    neighbourhoods_clean.append("Hermsdorf")

                elif str(neighbourhood).__contains__("Karow"):
                    print("Karow")
                    neighbourhoods_clean.append("Karow")

                elif str(neighbourhood).__contains__("Karlshorst"):
                    print("Karlshorst")
                    neighbourhoods_clean.append("Karlshorst")

                elif str(neighbourhood).__contains__("Kleinmachnow"):
                    print("Kleinmachnow")
                    neighbourhoods_clean.append("Kleinmachnow")

                elif str(neighbourhood).__contains__("Kreuzberg"):
                    print("Kreuzberg")
                    neighbourhoods_clean.append("Kreuzberg")

                elif str(neighbourhood).__contains__("kreuzberg"):
                    print("kreuzberg")
                    neighbourhoods_clean.append("Kreuzberg")

                elif str(neighbourhood).__contains__("Köpenick"):
                    print("Köpenick")
                    neighbourhoods_clean.append("Köpenick")

                elif str(neighbourhood).__contains__("Lankwitz"):
                    print("Lankwitz")
                    neighbourhoods_clean.append("Lankwitz")

                elif str(neighbourhood).__contains__("Lichtenberg"):
                    print("Lichtenberg")
                    neighbourhoods_clean.append("Lichtenberg")

                elif str(neighbourhood).__contains__("Lichterfelde"):
                    print("Lichterfelde")
                    neighbourhoods_clean.append("Lichterfelde")

                elif str(neighbourhood).__contains__("Marienfelde"):
                    print("Mitte")
                    neighbourhoods_clean.append("Marienfelde")

                elif str(neighbourhood).__contains__("Mariendorf"):
                    print("Mariendorf")
                    neighbourhoods_clean.append("Mariendorf")

                elif str(neighbourhood).__contains__("Marzahn"):
                    print("Marzahn")
                    neighbourhoods_clean.append("Marzahn")

                elif str(neighbourhood).__contains__("mitte"):
                    print("mitte")
                    neighbourhoods_clean.append("Mitte")

                elif str(neighbourhood).__contains__("Mitte"):
                    print("Mitte")
                    neighbourhoods_clean.append("Mitte")

                elif str(neighbourhood).__contains__("Moabit"):
                    print("Moabit")
                    neighbourhoods_clean.append("Moabit")

                elif str(neighbourhood).__contains__("Neukölln"):
                    print("Neukölln")
                    neighbourhoods_clean.append("Neukölln")

                elif str(neighbourhood).__contains__("Nikolassee"):
                    print("Nikolassee")
                    neighbourhoods_clean.append("Nikolassee")

                elif str(neighbourhood).__contains__("Niederschönhausen"):
                    print("Niederschönhausen")
                    neighbourhoods_clean.append("Niederschönhausen")

                elif str(neighbourhood).__contains__("Oberschöneweide"):
                    print("Oberschöneweide")
                    neighbourhoods_clean.append("Oberschöneweide")

                elif str(neighbourhood).__contains__("Pankow"):
                    print("Pankow")
                    neighbourhoods_clean.append("Pankow")

                elif str(neighbourhood).__contains__("Prenzlauer Berg"):
                    print("Prenzlauer Berg")
                    neighbourhoods_clean.append("Prenzlauer Berg")

                elif str(neighbourhood).__contains__("Reinickendorf"):
                    print("Reinickendorf")
                    neighbourhoods_clean.append("Reinickendorf")

                elif str(neighbourhood).__contains__("Rummelsburg"):
                    print("Rummelsburg")
                    neighbourhoods_clean.append("Rummelsburg")

                elif str(neighbourhood).__contains__("Siemensstadt"):
                    print("Siemensstadt")
                    neighbourhoods_clean.append("Siemensstadt")

                elif str(neighbourhood).__contains__("Schillerkiez"):
                    print("Schillerkiez")
                    neighbourhoods_clean.append("Schillerkiez")

                elif str(neighbourhood).__contains__("Schmargendorf"):
                    print("Schmargendorf")
                    neighbourhoods_clean.append("Schmargendorf")

                elif str(neighbourhood).__contains__("Schöneberg"):
                    print("Schöneberg")
                    neighbourhoods_clean.append("Schöneberg")

                elif str(neighbourhood).__contains__("Spandau"):
                    print("Spandau")
                    neighbourhoods_clean.append("Spandau")

                elif str(neighbourhood).__contains__("spandau"):
                    print("spandau")
                    neighbourhoods_clean.append("Spandau")

                elif str(neighbourhood).__contains__("Steglitz"):
                    print("Steglitz")
                    neighbourhoods_clean.append("Steglitz")

                elif str(neighbourhood).__contains__("Steglitz-Zehlendorf"):
                    print("Steglitz-Zehlendorf")
                    neighbourhoods_clean.append("Steglitz-Zehlendorf")

                elif str(neighbourhood).__contains__("Tegel"):
                    print("Tegel")
                    neighbourhoods_clean.append("Tegel")

                elif str(neighbourhood).__contains__("Tiergarten"):
                    print("Tiergarten")
                    neighbourhoods_clean.append("Tiergarten")

                elif str(neighbourhood).__contains__("Tempelhof"):
                    print("Tempelhof")
                    neighbourhoods_clean.append("Tempelhof")

                elif str(neighbourhood).__contains__("Treptow"):
                    print("Treptow")
                    neighbourhoods_clean.append("Treptow")

                elif str(neighbourhood).__contains__("Wannsee"):
                    print("Wannsee")
                    neighbourhoods_clean.append("Wannsee")

                elif str(neighbourhood).__contains__("Wedding"):
                    print("Wedding")
                    neighbourhoods_clean.append("Wedding")

                elif str(neighbourhood).__contains__("wedding"):
                    print("wedding")
                    neighbourhoods_clean.append("Wedding")

                elif str(neighbourhood).__contains__("Weißensee"):
                    print("Weißensee")
                    neighbourhoods_clean.append("Weißensee")

                elif str(neighbourhood).__contains__("Wilmersdorf"):
                    print("Wilmersdorf")
                    neighbourhoods_clean.append("Wilmersdorf")

                elif str(neighbourhood).__contains__("Zehlendorf"):
                    print("Zehlendorf")
                    neighbourhoods_clean.append("Zehlendorf")

                else:
                    neighbourhoods_clean.append(("Berlin"))
            df_concat["Neighbourhood"] = neighbourhoods_clean

            #Get periods of end dates
            df_concat['frei bis (Year - Month)'] = pd.to_datetime(df_concat['frei bis']).dt.to_period('M')
            print(neighbourhoods_clean)

            #Get locations of each neighbourhood
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

            #Export file
            if os.path.exists(nameofdataframe):
                st.write("Deleting existing csv output file")
                os.remove(nameofdataframe)
            else:
                st.write("No output file, continuing.")

            df_concat.to_csv(f"{nameofdataframe}")

            access_token = st.secrets.token
            repo_name = "wggesucht"
            g = Github(access_token)
            repo = g.get_user().get_repo(repo_name)
            csv_file = pd.read_csv(nameofdataframe)
            csv_file_string = csv_file.to_csv(index=False)
            csv_file_content = InputFileContent(csv_file_string)
            csv_file_content_str = str(csv_file_content)

            contents = repo.get_contents(nameofdataframe)

            repo.delete_file(nameofdataframe, "remove dataframe", contents.sha, branch="main")
            repo.create_file(nameofdataframe, "upload new dataframe", csv_file_string)
            st.write(f"Dataframe with name {nameofdataframe} uploaded.")
            # Notify the user that the file has been updated
            st.success(f"The file {nameofdataframe} has been updated!")
            button_pressed = False

            if button_pressed:
                st.write("Processing...")
            else:
                st.write("Ready to refresh again!")

        #Specify a path
        path = nameofdataframe
        # file modification timestamp of a file
        m_time = os.path.getctime(path)
        # convert timestamp into DateTime object
        dt_m = dt.datetime.fromtimestamp(m_time).strftime("%d/%m/%Y - %H:%M:%S")
        st.write(f'File last created on: {dt_m}')
        st.markdown("""---""")


    df_concat = pd.read_csv(nameofdataframe)

    #Filtering a bit more the dataframe
    dataframe_filter1 = df_concat["Größe"] > 9
    dataframe_filter2 = df_concat["Miete"] > 9
    df_concat = df_concat[dataframe_filter1]


    col1, col2 = st.columns([0.2, 0.8])
    with col1:
        st.markdown("<a href='https://www.linkedin.com/in/christian-h-0545aaa1/'>🔗 Find me on LinkedIn</a>", unsafe_allow_html=True)
        st.markdown("<a href='https://github.com/christianheins'>🔗 Find me on Github</a>", unsafe_allow_html=True)
    with col2:
        with st.expander("INSTRUCTIONS"):
            st.markdown("<h6 style='text-align: left; color: red;'>Instructions</h6>", unsafe_allow_html=True)
            st.markdown(f"<li style='text-align: left; color: grey; font-size: 12px;'>This web applications is capturing a snapshot of the last months entries as of the date the csv file was lastly refreshed from here: 'https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html?pagination=1&pu='</li>", unsafe_allow_html=True)
            st.markdown(f"<li style='text-align: left; color: grey; font-size: 12px;'>Please use as a guide for only the WG Gesucht portal, this data is not completly representative. It's just an example of the powerful features Steramlit has to offer. Logos and images are WG Gesuchts property and not mine.</li>", unsafe_allow_html=True)

    if selected == "🏘️ Apartments":
        st.markdown("<h1 style='text-align: center; color: orange;'>🏘️ Property Analysis 🏘</h1>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([0.2, 0.2, 0.6])
        with col1:
            st.metric("Available apartments", value="{:,.0f}".format(len(df_concat)))
        with col2:
            st.metric("Unique neighbourhoods", value="{:,.0f}".format(len(df_concat[['Rubrik', 'Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood']].pivot_table(index="Neighbourhood", values="Eintrag", aggfunc="count").reset_index())))
        with col3:
            df_concat['Eintrag'] = pd.to_datetime(df_concat['Eintrag'], format='%d.%m.%Y', dayfirst=True)
            oldestdate = df_concat["Eintrag"].min()
            st.metric("Oldest entry date", value=str(oldestdate))

        st.markdown("""---""")

        df_statistics = df_concat[["Miete", "Größe", 'EUR / SQM', "Lease term"]].describe()
        st.markdown("<h3 style='text-align: left; color: orange;'>📊 A little bit of Descriptive Statistics</h3>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

        with col1:
            st.metric("Average rent", value="{:,.0f} €".format(df_concat["Miete"].mean()))
        with col2:
            st.metric("Average size", value="{:,.0f} SQM".format(df_concat["Größe"].mean()))
        with col3:
            st.metric("Average EUR per SQM", value="{:,.0f} € per SQM".format(df_concat["EUR / SQM"].mean()))
        with col4:
            st.metric("Average lease term", value="{:,.0f} months".format(df_concat["Lease term"].mean()))

        with st.expander("Open for more"):

            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            with col1:
                #st.metric("Min rent", value="{:,.0f} €".format(df_concat["Miete"].min()))
                st.metric("Standard deviation rent", value="{:,.0f} €".format(df_concat["Miete"].std()))
                st.metric("25% of the leases are up to", value="{:,.0f} €".format(df_statistics.loc["25%"]["Miete"]))
                st.metric("50% of the leases are up to", value="{:,.0f} €".format(df_statistics.loc["50%"]["Miete"]))
                st.metric("75% of the leases are up to", value="{:,.0f} €".format(df_statistics.loc["75%"]["Miete"]))
                st.metric("Max rent", value="{:,.0f} €".format(df_concat["Miete"].max()))
            with col2:
                #st.metric("Min size", value="{:,.0f} SQM".format(df_concat["Größe"].min()))
                st.metric("Standard deviation size", value="{:,.0f} SQM".format(df_concat["Größe"].std()))
                st.metric("25% of the leases are up to", value="{:,.0f} SQM".format(df_statistics.loc["25%"]["Größe"]))
                st.metric("50% of the leases are up to", value="{:,.0f} SQM".format(df_statistics.loc["50%"]["Größe"]))
                st.metric("75% of the leases are up to", value="{:,.0f} SQM".format(df_statistics.loc["75%"]["Größe"]))
                st.metric("Max size", value="{:,.0f} SQM".format(df_concat["Größe"].max()))
            with col3:
                #st.metric("Min EUR per SQM", value="{:,.0f} € per SQM".format(df_concat["EUR / SQM"].min()))
                st.metric("Standard deviation EUR per SQM", value="{:,.0f} € per SQM".format(df_concat["EUR / SQM"].std()))
                st.metric("25% of the leases are up to", value="{:,.0f} € per SQM".format(df_statistics.loc["25%"]["EUR / SQM"]))
                st.metric("50% of the leases are up to", value="{:,.0f} € per SQM".format(df_statistics.loc["50%"]["EUR / SQM"]))
                st.metric("75% of the leases are up to", value="{:,.0f} € per SQM".format(df_statistics.loc["75%"]["EUR / SQM"]))
                st.metric("Max EUR per SQM", value="{:,.0f} € per SQM".format(df_concat["EUR / SQM"].max()))
            with col4:
                #st.metric("Min lease term", value="{:,.0f} months".format(df_concat["Lease term"].min()))
                st.metric("Standard deviation lease term", value="{:,.0f} months".format(df_concat["Lease term"].std()))
                st.metric("25% of the leases are up to", value="{:,.0f} months".format(df_statistics.loc["25%"]["Lease term"]))
                st.metric("50% of the leases are up to", value="{:,.0f} months".format(df_statistics.loc["50%"]["Lease term"]))
                st.metric("75% of the leases are up to", value="{:,.0f} months".format(df_statistics.loc["75%"]["Lease term"]))
                st.metric("Longest lease term", value="{:,.0f} months".format(df_concat["Lease term"].max()))

            st.markdown("<h6 style='text-align: left; color: orange;'>Numerical values described</h6>", unsafe_allow_html=True)
            st.write(df_concat[["Miete", "Größe", 'EUR / SQM', "Lease term"]].describe())

        st.markdown("""---""")
        df_concat_neighbourhoods = df_concat[['Rubrik', 'Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood']].pivot_table(index="Neighbourhood", values="Eintrag", aggfunc="count").reset_index()
        df_concat_neighbourhoods.sort_values(by=["Eintrag"], ascending=[False], inplace=True)

        df_concat_endofleaseterm = df_concat[['Rubrik', 'Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood', 'Lease term']].pivot_table(index="Lease term", values="Eintrag", aggfunc="count").reset_index()
        df_concat_endofleaseterm.sort_values(by=["Eintrag"], ascending=[False], inplace=True)

        col1, col2, col3= st.columns([0.3, 0.3, 0.3])
        with col1:
            df_concat_pivot_longterm = df_concat["Lease term"].isna().sum()
            df_concat_pivot_shortterm = len(df_concat[df_concat["Lease term"] > 0])
            source = pd.DataFrame({"Category": ["Indefinite term", "Limited term"], "Value": [df_concat_pivot_longterm, df_concat_pivot_shortterm]})
            st.markdown("<h6 style='text-align: center; color: orange;'>Lease term Donut</h6>", unsafe_allow_html=True)

            chart = alt.Chart(source).mark_arc(innerRadius=90).encode(
                theta='Value:Q',
                color=alt.Color('Category', scale=alt.Scale(scheme='category10')),
                tooltip=['Value:Q'],
            )
            chart = chart.configure_legend(
                orient='left'
            )
            st.altair_chart(chart.interactive(), use_container_width=True)

            st.markdown("<h6 style='text-align: center; color: orange;'>Lease term Bar Chart</h6>", unsafe_allow_html=True)
            chart = alt.Chart(df_concat_endofleaseterm).encode(
                x=alt.X('Lease term:Q'),
                y=alt.Y('Eintrag:Q', sort=None), #use 'sort=None' to preserve the order of categories
                text=alt.Text('Eintrag', format='.1f')
            )
            #Combine bar chart with text chart, weird isnt?
            wholechart = alt.layer(chart.mark_bar(color="orange"), chart.mark_text(align='center', dy=-5, color="black"))

            st.altair_chart(wholechart.interactive(), use_container_width=True)

        with col2:
            st.markdown("<h6 style='text-align: center; color: orange;'>Top 10 Neighbourhoods by count</h6>", unsafe_allow_html=True)

            df_concat_neighbourhoods_filtered = df_concat_neighbourhoods.iloc[:10]

            chart = alt.Chart(df_concat_neighbourhoods_filtered).mark_arc(innerRadius=90).encode(
                theta='Eintrag:Q',
                color=alt.Color('Neighbourhood', scale=alt.Scale(scheme='category10')),
                tooltip=['Neighbourhood', 'Eintrag:Q'],
            )

            chart = chart.configure_legend(
                orient='left'
            )
            st.altair_chart(chart.interactive(), use_container_width=True)

            df_concat_neighbourhoods_filtered = df_concat_neighbourhoods.iloc[:20]
            chart = alt.Chart(df_concat_neighbourhoods_filtered).encode(
                x=alt.X('Eintrag:Q'),
                y=alt.Y('Neighbourhood:N', sort=None), #use 'sort=None' to preserve the order of categories
                text=alt.Text('Eintrag:Q', format='.1f'),
            )
            #Combine bar chart with text chart, weird isnt?

            #wholechart = chart.mark_bar(color="orange") + chart.mark_text(align='left', dx=8, color="black")

            wholechart = alt.layer(chart.mark_bar(color="orange"), chart.mark_text(align='left', dx=8, color="black"))

            st.markdown("<h6 style='text-align: center; color: orange;'>Top 20 Neighbourhoods Bar Chart</h6>", unsafe_allow_html=True)
            st.altair_chart(wholechart.interactive(), use_container_width=True)

        with col3:
            st.markdown("<h6 style='text-align: center; color: orange;'>Release dates</h6>", unsafe_allow_html=True)
            chart = alt.Chart(source).mark_arc(innerRadius=90).encode(
                    theta='Value:Q',
                    color=alt.Color('Category', scale=alt.Scale(scheme='category10')),
                    tooltip=['Value:Q'],
                )
            chart = chart.configure_legend(
                orient='left'
            )
            st.altair_chart(chart.interactive(), use_container_width=True)
            df_concat_pivot_releasedate = df_concat[['Rubrik', 'Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood']].pivot_table(index="Eintrag", values="Miete", aggfunc={"Miete":["count","mean"]}).reset_index()
            df_concat_pivot_releasedate['Eintrag'] = pd.to_datetime(df_concat_pivot_releasedate['Eintrag'], format='%d.%m.%Y', dayfirst=True)
            df_concat_pivot_releasedate.sort_values(by=["Eintrag"], ascending=[False], inplace=True)
            df_concat_pivot_releasedate['Eintrag'] = df_concat_pivot_releasedate['Eintrag'].dt.strftime('%Y/%m/%d')

            st.markdown("<h6 style='text-align: center; color: orange;'>Number of entries per release date</h6>", unsafe_allow_html=True)

            chart = alt.Chart(df_concat_pivot_releasedate).encode(
                x=alt.X('count:Q'),
                y=alt.Y('Eintrag:N', sort=None), #use 'sort=None' to preserve the order of categories
                text=alt.Text('count', format='.1f')
            )
            #Combine bar chart with text chart, weird isnt?

            #wholechart = chart.mark_bar(color="orange") + chart.mark_text(align='left', dx=8, color="black")

            wholechart = alt.layer(chart.mark_bar(color="orange"), chart.mark_text(align='left', dx=8, color="black"))

            st.altair_chart(wholechart.interactive(), use_container_width=True)
        st.markdown("<h2 style='text-align: center; color: orange;'>💥 Scatter plots displaying the Price / Size relationship</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns([0.5,0.5])

        with col1:
            chart = alt.Chart(df_concat).mark_point().encode(
                x=alt.X('Größe:Q', title='Size', axis=alt.Axis(tickCount=5)),
                y=alt.Y('Miete:Q', title='Rent', axis=alt.Axis(tickCount=5)),
                tooltip=['Größe', 'Miete']
            )
            # show the chart
            st.altair_chart(chart.interactive(), use_container_width=True)
        with col2:
            chart = alt.Chart(df_concat).mark_point().encode(
                x=alt.X('Größe:Q', title='Size', axis=alt.Axis(tickCount=5)),
                y=alt.Y('Miete:Q', title='Rent', axis=alt.Axis(tickCount=5)),
                tooltip=['Größe', 'Miete']
            )
            # show the chart
            st.altair_chart(chart.interactive(), use_container_width=True)

        st.markdown("<h6 style='text-align: center; color: orange;'>Properties table</h6>", unsafe_allow_html=True)
        st.write(df_concat[['Name', 'Rubrik', 'Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood', 'frei ab', 'frei bis','frei bis (Year - Month)', 'Lease term', 'Latitude', 'Longitude']])

        st.markdown("""---""")
        st.markdown("<h3 style='text-align: center; color: orange;'>Map of neighbourhoods</h6>", unsafe_allow_html=True)

        #df_concat.drop(df_concat[df_concat["Latitude"].str() != "Location not found: NA"], inplace=True)
        latitudes = ["Location not found: Wedding","Location not found: Reinickendorf","Location not found: Prenzlauer Berg","Location not found: Neukölln","Location not found: NA","Location not found: Moabit","Location not found: Mitte","Location not found: Marienfelde","Location not found: Lichtenberg","Location not found: Kreuzberg","Location not found: Charlottenburg"]
        df_concat = df_concat[~df_concat["Latitude"].isin(latitudes)]
        df_concat.rename(columns = {"Latitude":"lat","Longitude":"lon"}, inplace=True)
        df_concat['lat'] = pd.to_numeric(df_concat['lat'])
        df_concat['lon'] = pd.to_numeric(df_concat['lon'])
        st.map(df_concat)

        with st.container():
            st.write("This is inside the container")

            # You can call any Streamlit command, including custom components:
            st.bar_chart(np.random.randn(50, 3))

        st.write("This is outside the container")

        st.header("📈 Rent timeline")

        df_old = pd.read_csv("df_concat_20230412.csv")
        df_old["Dataframe Date"] = "20230412"

        df_concat["Dataframe Date"] = "20230420"

        df_timeline = pd.concat([df_concat, df_old])
        st.write(df_timeline)
        st.write(len(df_timeline))
        df_timeline_pivotedby_dataframedate = df_timeline.pivot_table(index="Dataframe Date", aggfunc={"Miete":["mean","sum"]}).reset_index()
        st.write(df_timeline_pivotedby_dataframedate)
        st.write(df_timeline_pivotedby_dataframedate.columns.values)
        miete_average = df_timeline_pivotedby_dataframedate.columns.values[1]
        st.write(miete_average)
        miete_sum = str(df_timeline_pivotedby_dataframedate.columns.values[2])
        st.write(miete_sum)

        df_timeline_pivotedby_dataframedate.rename(columns = {miete_average:"Average", miete_sum:"Sum", "Dataframe Date":"Dataframe Date 2"}, inplace=True)

        st.write(df_timeline_pivotedby_dataframedate)
        st.write(df_timeline_pivotedby_dataframedate.columns)
        col1, col2, col3 = st.columns([0.3, 0.3, 0.3])
        with col1:

            chart = alt.Chart(df_timeline_pivotedby_dataframedate).mark_line(
                color="red"
            ).encode(
                x='Dataframe Date 2:O',
                y=alt.Y('Average:Q'),
            ).interactive()

            chart2 = alt.Chart(df_timeline_pivotedby_dataframedate).mark_bar(
                color="#95B5C3",
                opacity=0.5,
            ).encode(
                x='Dataframe Date 2:O',
                y=alt.Y('Average:Q'),
            ).interactive()


            chart = (chart + chart2)
            chart = chart
            st.altair_chart(chart, use_container_width=True)

        with col2:
            limit_min = float(df_kontoauswertung_pivoted_by_contract_pivoted_by_period["Bruttowarmmiete"].min()) - (float(df_kontoauswertung_pivoted_by_contract_pivoted_by_period["Bruttowarmmiete"].min()) * 0.03)
            limit_max = float(df_kontoauswertung_pivoted_by_contract_pivoted_by_period["Bruttowarmmiete"].max()) + (float(df_kontoauswertung_pivoted_by_contract_pivoted_by_period["Bruttowarmmiete"].max()) * 0.03)

            chart = alt.Chart(df_kontoauswertung_pivoted_by_contract_pivoted_by_period).mark_line(
                color="red"
            ).encode(
                x='year_month',
                y=alt.Y('Bruttowarmmiete', scale=alt.Scale(domain=[limit_min, limit_max])),
            ).interactive()

            chart2 = alt.Chart(df_kontoauswertung_pivoted_by_contract_pivoted_by_period).mark_bar(
                color="#95B5C3",
                opacity=0.5,
            ).encode(
                x='year_month:O',
                y=alt.Y("Bruttowarmmiete:Q", scale=alt.Scale(domain=[limit_min, limit_max])),
            ).interactive()


            chart = (chart + chart2)
            chart = chart
            st.altair_chart(chart, use_container_width=True)

        with col3:
            limit_min = float(df_kontoauswertung_pivoted_by_contract_pivoted_by_period["Bruttowarmmiete"].min()) - (float(df_kontoauswertung_pivoted_by_contract_pivoted_by_period["Bruttowarmmiete"].min()) * 0.03)
            limit_max = float(df_kontoauswertung_pivoted_by_contract_pivoted_by_period["Bruttowarmmiete"].max()) + (float(df_kontoauswertung_pivoted_by_contract_pivoted_by_period["Bruttowarmmiete"].max()) * 0.03)

            chart = alt.Chart(df_kontoauswertung_pivoted_by_contract_pivoted_by_period).mark_line(
                color="red"
            ).encode(
                x='year_month',
                y=alt.Y('Bruttowarmmiete', scale=alt.Scale(domain=[limit_min, limit_max])),
            ).interactive()

            chart2 = alt.Chart(df_kontoauswertung_pivoted_by_contract_pivoted_by_period).mark_bar(
                color="#95B5C3",
                opacity=0.5,
            ).encode(
                x='year_month:O',
                y=alt.Y("Bruttowarmmiete:Q", scale=alt.Scale(domain=[limit_min, limit_max])),
            ).interactive()


            chart = (chart + chart2)
            chart = chart
            st.altair_chart(chart, use_container_width=True)



    if selected == "🫂 Neighbourhoods":
        st.markdown("<h1 style='text-align: center; color: orange;'>Neighbourhood Analysis</h1>", unsafe_allow_html=True)
        st.write(df_concat)
        df_concat_pivot_neighbourhoods = df_concat.pivot_table(index="Neighbourhood", aggfunc={"Miete":["count","mean","sum"], "Größe":["count", "mean", "sum"]})
        st.write(df_concat_pivot_neighbourhoods)

    if selected == "📑 Sample contracts":
        st.markdown("<h1 style='text-align: center; color: orange;'>Neighbourhood Analysis</h1>", unsafe_allow_html=True)
        st.write(df_concat)
        df_concat_pivot_neighbourhoods = df_concat.pivot_table(index="Neighbourhood", aggfunc={"Miete":["count","mean","sum"], "Größe":["count", "mean", "sum"]})
        st.write(df_concat_pivot_neighbourhoods)

    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
