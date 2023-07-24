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
    import datetime
    import base64
    from github import Github
    from github import InputFileContent
    import smtplib, email
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.utils import COMMASPACE, formatdate
    from email.mime.image import MIMEImage
    import ssl
    import slack
    import pytz

    #Streamlit


    st.set_page_config(page_title="WG Gesucht Analysis", layout="wide", initial_sidebar_state="expanded", menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })


    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    pd.set_option('display.max_columns', None)

    nameofdataframe = "df_concat.csv"

    with st.sidebar:
        st.sidebar.header("Sections")
        selected = option_menu(
            menu_title="Menu",
            options=["🏘️ Apartments", "🫂 Neighbourhoods", "📑 Sample contracts"], #https://icons.getbootstrap.com/
            orientation="vertical",
        )

        # Create a button
        button_pressed = False
        st.markdown("""---""")
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
                    df['Lease term'] = (df['frei bis'].dt.year - df['frei ab'].dt.year) * 12 + (df['frei bis'].dt.month - df['frei ab'].dt.month)
                    df["EUR / SQM"] = df["Miete"] / df["Größe"]

                    df_toupdate.append(df)

                df = pd.concat(df_toupdate)
                return df

            df_concat = requestswg_all()
            df_concat.dropna(subset=["Eintrag"], inplace=True)
            df_concat.reset_index(drop=True, inplace=True)

            #Give eachrow a name
            def combine_names(row):
                return str(row['Data ID']) + str(row['Eintrag']) + '-' + str(row['Miete'])  + '-' + str(row['EUR / SQM']) + ' ' + str(row['Stadtteil'])

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

        # Specify a path
        path = nameofdataframe
        # file modification timestamp of a file
        m_time = os.path.getctime(path)

        # Convert timestamp into DateTime object
        dt_m = datetime.datetime.fromtimestamp(m_time).strftime("%d/%m/%Y - %H:%M:%S")
        st.write(f'File last created on: {dt_m}')
        st.markdown("""---""")


    df_concat = pd.read_csv(nameofdataframe)
    df_concat.drop(columns=["Unnamed: 0.1", "Unnamed: 0"], inplace=True)
    df_concat.rename(columns = {"index":"Data ID", "Posting Date":"Eintrag", "Price":"Miete", "Size":"Größe","Date From":"frei ab", "Date To":"frei bis", "Location":"Stadtteil", "Date To (Year - Month)":"frei bis (Year - Month)"}, inplace=True)
    df_immowelt = pd.read_csv("df_immowelt.csv")
    df_concat = pd.concat([df_concat, df_immowelt])
    st.write(df_concat)

    #st.write(df_concat)
    #st.write(df_concat.columns)


    # Filtering a bit more the dataframe
    dataframe_filter1 = df_concat["Größe"] > 9
    dataframe_filter2 = df_concat["Miete"] > 9
    df_concat = df_concat[dataframe_filter1]
    st.header("🚧 SAL MAGUDA - WORK IN PROGRESS")

    with st.expander("DISCLAIMER"):
        st.markdown("<h6 style='text-align: left; color: red;'>Instructions</h6>", unsafe_allow_html=True)
        st.markdown(f"<li style='text-align: left; color: grey; font-size: 12px;'>This web applications is capturing a snapshot of the last months entries as of the date the csv file was lastly refreshed from here: 'https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html?pagination=1&pu='</li>", unsafe_allow_html=True)
        st.markdown(f"<li style='text-align: left; color: grey; font-size: 12px;'>Please use as a guide for only the WG Gesucht portal, this data is not completly representative. It's just an example of the powerful features Steramlit has to offer. Logos and images are WG Gesuchts property and not mine.</li>", unsafe_allow_html=True)

    col1, col2 = st.columns([0.2, 0.8])
    with col1:
        st.markdown("<a href='https://www.linkedin.com/in/christian-h-0545aaa1/'>🔗 Find me on LinkedIn</a>", unsafe_allow_html=True)
        st.markdown("<a href='https://github.com/christianheins'>🔗 Find me on Github</a>", unsafe_allow_html=True)
    with col2:
        text = st.text_input("Send me a message on slack 💬")
        def sendslack():
            #Create a slack client and define todays date or moment date
            client = slack.WebClient(token=st.secrets.slack_bot_token)

            #Tell the client to select a channel and include the specified text.
            client.chat_postMessage(channel='#special-projects', text=f"Message from an user:\n\n{text}")
            print("Sending slack message")
        button2 = st.button("Send message")
        if button2:
            sendslack()
            st.success("Message sent!")
        button2 = False


    if selected == "🏘️ Apartments":
        st.markdown("<h1 style='text-align: center; color: orange;'>Property Analysis 🏘</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: left; color: black;'>Scraped websites</h3>", unsafe_allow_html=True)

        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            text = " This is a website that showcases the capabilities of Streamlit, a powerful Python library for building interactive web applications. With Streamlit, we can transform scraped data into meaningful visualizations, charts, and tables, making it easier to communicate and share our findings with others. \n\n To retrieve data from websites, we leverage other Python libraries such as Requests and Beautiful Soup. The Requests library allows us to send GET and POST requests, retrieving the HTML content of a webpage. We then utilize the Beautiful Soup library to parse and navigate the HTML tree structure, making it easy to locate and extract specific elements or data. By combining Streamlit with these web scraping techniques, we can automate the process of gathering data from websites and create valuable resources for analysis, research, and decision-making. We can continuously scrape websites, storing the collected data to build and expand huge databases over time. Furthermore, web scraping techniques such as pagination, form submission, or dynamic content loading enable us to access and gather data from even the most complex websites. \n\n We leverage other Python libraries like pandas to further enhance our data manipulation and analysis capabilities. Pandas is a popular library for data manipulation and analysis, providing a wide range of functions and methods to handle and transform data efficiently. With pandas, we can easily load the scraped data into a structured format called a DataFrame. This allows us to perform various data transformations, such as filtering, sorting, and joining, to clean and prepare the data for analysis. We can also handle missing values, perform data type conversions, and rename columns, ensuring that the data is in a suitable format for further analysis. \n\n This versatility in data acquisition empowers us to perform several data analysis tasks, uncover insights, track trends, and gain a competitive edge in various domains and industries. Streamlit provides a seamless user experience, allowing us to create interactive dashboards and present the scraped data in a visually appealing manner. With Streamlit, we can easily showcase the extracted information through visualizations, charts, and tables, making it simple to communicate and share our findings effectively."

            st.markdown(f"<p style='text-align: left; color: black;'>{text}</p>", unsafe_allow_html=True)
        with col2:
            st.markdown("<img src='https://content.cdn.immowelt.com/iw_group/_processed_/c/5/csm_immowelt-Logo-thumb_262f254ba2.png' width=300></img>", unsafe_allow_html=True)
            st.markdown("<img src='https://www.lautgegennazis.de/wp-content/uploads/2016/10/WG_Banner.jpg' width=300></img>", unsafe_allow_html=True)
            st.markdown("<img src='https://content.cdn.immowelt.com/iw_group/_processed_/9/b/csm_logo-rgb-immonet_c1dfb328a4.png' width=300></img>", unsafe_allow_html=True)

        st.markdown("<h6 style='text-align: center; color: orange;'>Properties table</h6>", unsafe_allow_html=True)
        with st.expander("Table"):

            df_concat["Link"] = "https://"+df_concat["Link"]
            st.write(df_concat.columns.to_list())

            st.dataframe(df_concat[["Data ID", "Eintrag", "City", "Neighbourhood", "Address", "Miete" , "Größe", "EUR / SQM", "Deposit", "frei ab", "frei bis", "frei bis (Year - Month)", "Lease term","DataFrame", "Latitude", "Longitude", "Link", "Stadtteil", "Neighbourhood (Dirty)"]],
                         column_config={
                            "Data ID": st.column_config.NumberColumn(format="%d"),
                            "Miete": st.column_config.NumberColumn(format="%d €"),
                            "Größe": st.column_config.NumberColumn(format="%d SQM"),
                            "EUR / SQM": st.column_config.NumberColumn(format="%.2f €"),
                            "Deposit": st.column_config.NumberColumn(format="%d €"),
                            "Link": st.column_config.LinkColumn("Link"),
                            "DataFrame": st.column_config.NumberColumn(format="%d"),
                            "Lease term": st.column_config.NumberColumn(format="%d Months"),
                            "City": st.column_config.ListColumn("City"),
                            "Neighbourhood": st.column_config.ListColumn("Neighbourhood"),
                            }
                         )

        col1, col2, col3, col4 = st.columns([0.2, 0.2, 0.35, 0.35])
        with col1:
            st.metric("Available apartments", value="{:,.0f}".format(len(df_concat)))
        with col2:
            st.metric("Unique neighbourhoods", value="{:,.0f}".format(len(df_concat[['Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood']].pivot_table(index="Neighbourhood", values="Eintrag", aggfunc="count").reset_index())))
        with col3:
            df_concat['Eintrag'] = pd.to_datetime(df_concat['Eintrag'], format='%d.%m.%Y', dayfirst=True)
            oldestdate = df_concat["Eintrag"].min()
            st.metric("Oldest entry date", value=str(oldestdate))
        with col4:
            df_concat['Eintrag'] = pd.to_datetime(df_concat['Eintrag'], format='%d.%m.%Y', dayfirst=True)
            oldestdate = df_concat["Eintrag"].max()
            st.metric("Max entry date", value=str(oldestdate))

        st.markdown("""---""")

        df_concat_neighbourhoods = df_concat[['Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood']].pivot_table(index="Neighbourhood", values="Eintrag", aggfunc="count").reset_index()
        df_concat_neighbourhoods.sort_values(by=["Eintrag"], ascending=[False], inplace=True)

        df_concat_endofleaseterm = df_concat[['Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood', 'Lease term']].pivot_table(index="Lease term", values="Eintrag", aggfunc="count").reset_index()
        df_concat_endofleaseterm.sort_values(by=["Eintrag"], ascending=[False], inplace=True)

        col1, col2, col3= st.columns([0.3, 0.3, 0.3])
        with col1:

            # Add a
            df_concat_neighbourhoods_filtered = df_concat_neighbourhoods.iloc[:20]

            chart = alt.Chart(df_concat_neighbourhoods_filtered).encode(
                x=alt.X('Eintrag:Q', axis=alt.Axis(title='Count')),
                y=alt.Y('Neighbourhood:N', sort=None), #use 'sort=None' to preserve the order of categories
                text=alt.Text('Eintrag:Q', format='.1f'),
            )
            #Combine bar chart with text chart, weird isnt?

            #wholechart = chart.mark_bar(color="orange") + chart.mark_text(align='left', dx=8, color="black")

            wholechart = alt.layer(chart.mark_bar(color="orange"), chart.mark_text(align='left', dx=8, color="black"))

            wholechart = wholechart.properties(
                height=500
            )

            st.markdown("<h6 style='text-align: center; color: orange;'>Top 20 Neighbourhoods Bar Chart</h6>", unsafe_allow_html=True)
            st.altair_chart(wholechart.interactive(), use_container_width=True)

            st.markdown("<h6 style='text-align: center; color: orange;'>Lease term Bar Chart</h6>", unsafe_allow_html=True)

            chart = alt.Chart(df_concat_endofleaseterm).encode(
                x=alt.X('Lease term:Q'),
                y=alt.Y('Eintrag:Q', sort=None, axis=alt.Axis(title='Count')), #use 'sort=None' to preserve the order of categories
                text=alt.Text('Eintrag', format='.1f')
            )

            # Combine bar chart with text chart, weird isnt?
            wholechart = alt.layer(chart.mark_bar(color="orange"), chart.mark_text(align='center', dy=-5, color="black"))
            wholechart = wholechart.properties(
                height=500
            )

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

            chart = chart.properties(
                height=300
            )

            st.altair_chart(chart.interactive(), use_container_width=True)

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

            chart = chart.properties(
                height=300
            )
            st.altair_chart(chart.interactive(), use_container_width=True)

        with col3:
            df_concat_pivot_releasedate = df_concat[['Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood']].pivot_table(index="Neighbourhood", values="Miete", aggfunc={"Miete":["count","mean"]}).reset_index()

            chart = alt.Chart(df_concat_pivot_releasedate).encode(
                x=alt.X('mean:Q', axis=alt.Axis(title='Average Euro per advert')),
                y=alt.Y('Neighbourhood:N', sort=None), #use 'sort=None' to preserve the order of categories
                text=alt.Text('mean:Q', format='.1f'),
            )
            #Combine bar chart with text chart, weird isnt?

            #wholechart = chart.mark_bar(color="orange") + chart.mark_text(align='left', dx=8, color="black")

            wholechart = alt.layer(chart.mark_bar(color="orange"), chart.mark_text(align='left', dx=8, color="black"))

            wholechart = wholechart.properties(
                height=300
            )
            st.markdown("<h6 style='text-align: center; color: orange;'>Average Rent per Neighbourhood</h6>", unsafe_allow_html=True)
            st.altair_chart(wholechart.interactive(), use_container_width=True)

            df_concat_pivot_releasedate = df_concat[['Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood']].pivot_table(index="Eintrag", values="Miete", aggfunc={"Miete":["count","mean"]}).reset_index()
            df_concat_pivot_releasedate['Eintrag'] = pd.to_datetime(df_concat_pivot_releasedate['Eintrag'], format='%d.%m.%Y', dayfirst=True)
            df_concat_pivot_releasedate.sort_values(by=["Eintrag"], ascending=[False], inplace=True)
            df_concat_pivot_releasedate['Eintrag'] = df_concat_pivot_releasedate['Eintrag'].dt.strftime('%Y/%m/%d')

            st.markdown("<h6 style='text-align: center; color: orange;'>Number of entries per release date</h6>", unsafe_allow_html=True)
            chart = alt.Chart(df_concat_pivot_releasedate).encode(
                x=alt.X('count:Q', axis=alt.Axis(title='Count')),
                y=alt.Y('Eintrag:T', sort=None, axis=alt.Axis(title='Entry date')), #use 'sort=None' to preserve the order of categories
                text=alt.Text('count', format='.1f')
            )
            #Combine bar chart with text chart, weird isnt?

            #wholechart = chart.mark_bar(color="orange") + chart.mark_text(align='left', dx=8, color="black")

            wholechart = alt.layer(chart.mark_bar(color="orange"), chart.mark_text(align='left', dx=8, color="black"))
            wholechart = wholechart.properties(
                height=500
            )
            st.altair_chart(wholechart.interactive(), use_container_width=True)


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
                chart = alt.Chart(df_concat).mark_boxplot().encode(
                    y='Miete:Q'
                ).properties(
                    height=400,
                    width=100
                )
                st.altair_chart(chart)
                st.metric("Standard deviation rent", value="{:,.0f} €".format(df_concat["Miete"].std()))
                st.metric("25% of the leases are up to", value="{:,.0f} €".format(df_statistics.loc["25%"]["Miete"]))
                st.metric("50% of the leases are up to", value="{:,.0f} €".format(df_statistics.loc["50%"]["Miete"]))
                st.metric("75% of the leases are up to", value="{:,.0f} €".format(df_statistics.loc["75%"]["Miete"]))
                st.metric("Max rent", value="{:,.0f} €".format(df_concat["Miete"].max()))


            with col2:
                #st.metric("Min size", value="{:,.0f} SQM".format(df_concat["Größe"].min()))
                chart = alt.Chart(df_concat).mark_boxplot().encode(
                    y=alt.Y('Größe:Q', title="Size in SQM")
                ).properties(
                    height=400,
                    width=100
                )
                st.altair_chart(chart)
                st.metric("Standard deviation size", value="{:,.0f} SQM".format(df_concat["Größe"].std()))
                st.metric("25% of the leases are up to", value="{:,.0f} SQM".format(df_statistics.loc["25%"]["Größe"]))
                st.metric("50% of the leases are up to", value="{:,.0f} SQM".format(df_statistics.loc["50%"]["Größe"]))
                st.metric("75% of the leases are up to", value="{:,.0f} SQM".format(df_statistics.loc["75%"]["Größe"]))
                st.metric("Max size", value="{:,.0f} SQM".format(df_concat["Größe"].max()))
            with col3:
                #st.metric("Min EUR per SQM", value="{:,.0f} € per SQM".format(df_concat["EUR / SQM"].min()))
                chart = alt.Chart(df_concat).mark_boxplot().encode(
                    y='EUR / SQM:Q'
                ).properties(
                    height=400,
                    width=100
                )
                st.altair_chart(chart)
                st.metric("Standard deviation EUR per SQM", value="{:,.0f} € per SQM".format(df_concat["EUR / SQM"].std()))
                st.metric("25% of the leases are up to", value="{:,.0f} € per SQM".format(df_statistics.loc["25%"]["EUR / SQM"]))
                st.metric("50% of the leases are up to", value="{:,.0f} € per SQM".format(df_statistics.loc["50%"]["EUR / SQM"]))
                st.metric("75% of the leases are up to", value="{:,.0f} € per SQM".format(df_statistics.loc["75%"]["EUR / SQM"]))
                st.metric("Max EUR per SQM", value="{:,.0f} € per SQM".format(df_concat["EUR / SQM"].max()))
            with col4:
                #st.metric("Min lease term", value="{:,.0f} months".format(df_concat["Lease term"].min()))
                chart = alt.Chart(df_concat ).mark_boxplot().encode(
                    y=alt.Y('Lease term:Q', title="Lease term in months")
                ).properties(
                    height=400,
                    width=100
                )
                st.altair_chart(chart)
                st.metric("Standard deviation lease term", value="{:,.0f} months".format(df_concat["Lease term"].std()))
                st.metric("25% of the leases are up to", value="{:,.0f} months".format(df_statistics.loc["25%"]["Lease term"]))
                st.metric("50% of the leases are up to", value="{:,.0f} months".format(df_statistics.loc["50%"]["Lease term"]))
                st.metric("75% of the leases are up to", value="{:,.0f} months".format(df_statistics.loc["75%"]["Lease term"]))
                st.metric("Longest lease term", value="{:,.0f} months".format(df_concat["Lease term"].max()))

            st.markdown("<h6 style='text-align: left; color: orange;'>Numerical values described</h6>", unsafe_allow_html=True)
            st.write(df_concat[["Miete", "Größe", 'EUR / SQM', "Lease term"]].describe())

        st.markdown("""---""")

        selected = option_menu(
            menu_title="⏱️ Lease term",
            options=["🕳️ All", "🍆 Long term", "🩳 Short term"], #https://icons.getbootstrap.com/
            orientation="horizontal",
        )


        st.markdown("<h4 style='text-align: center; color: orange;'>💥 Scatter plots displaying the Rent / Size relationship</h4>", unsafe_allow_html=True)

        col1, col2 = st.columns([0.5,0.5])

        with col1:
            chart = alt.Chart(df_concat).mark_point(color="orange").encode(
                x=alt.X('Größe:Q', title='Size', axis=alt.Axis(tickCount=5)),
                y=alt.Y('Miete:Q', title='Rent', axis=alt.Axis(tickCount=5)),
                tooltip=['Größe', 'Miete']

            )
            # show the chart
            st.altair_chart(chart.interactive(), use_container_width=True)

            chart = alt.Chart(df_concat).mark_point(color="orange").encode(
                x=alt.X('EUR / SQM:Q', title='EURO per SQM', axis=alt.Axis(tickCount=5)),
                y=alt.Y('Lease term:Q', title='Lease term', axis=alt.Axis(tickCount=5)),
                tooltip=['Lease term', 'EUR / SQM', 'Name', 'Link']
            )
            # show the chart
            st.altair_chart(chart.interactive(), use_container_width=True)

        with col2:
            chart = alt.Chart(df_concat).mark_point(color="orange").encode(
                x=alt.X('Größe:Q', title='Size', axis=alt.Axis(tickCount=5), scale=alt.Scale(reverse=True)),
                y=alt.Y('EUR / SQM:Q', title='Rent per SQM', axis=alt.Axis(tickCount=5)),
                tooltip=['Miete', 'Größe', 'EUR / SQM', 'Neighbourhood', 'Link', 'Lease term']
            )
            # show the chart
            st.altair_chart(chart.interactive(), use_container_width=True)

            chart = alt.Chart(df_concat[df_concat["Lease term"]>0]).mark_point(color="orange").encode(
                x=alt.X('Lease term:Q', title='Lease term', axis=alt.Axis(tickCount=5), scale=alt.Scale(reverse=True)),
                y=alt.Y('EUR / SQM:Q', title='EUR per SQM', axis=alt.Axis(tickCount=5)),
                tooltip=['Neighbourhood', 'EUR / SQM', 'Link', 'Lease term']
            )
            # show the chart
            st.altair_chart(chart.interactive(), use_container_width=True)

            chart = alt.Chart(df_concat).mark_point(color="orange").encode(
                x=alt.X('Neighbourhood:N', title='Neighbourhood', axis=alt.Axis(tickCount=5)),
                y=alt.Y('EUR / SQM:Q', title='Rent per SQM', axis=alt.Axis(tickCount=5)),
                tooltip=['Neighbourhood', 'EUR / SQM']
            )
            # show the chart
            st.altair_chart(chart.interactive(), use_container_width=True)

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

        df_2023_05 = pd.read_csv("df_concat_20230531.csv")
        df_2023_05["Dataframe Date"] = "20230531"
        df_2023_05["Size"] = df_2023_05["Größe"]
        df_2023_05.rename(columns={"Unnamed: 8":"Dataframe","Unnamed: 0.1":"Data ID", "Unnamed: 0":"Link", "Latitude":"lat", "Longitude":"lon", "Miete":"Pure Rent"}, inplace=True)
        df_2023_05.reset_index(drop=True, inplace=True)

        df_2023_06 = pd.read_csv("df_concat_20230630.csv")
        df_2023_06.rename(columns={"index":"Data ID", "DataFrame": "Dataframe Date", "Pure rent": "Pure Rent"}, inplace=True)
        df_2023_06["Dataframe Date"] = "20230630"
        df_2023_06["Pure Rent"] = df_2023_06["Price"]
        df_2023_06.reset_index(drop=True, inplace=True)

        df_2023_07 = pd.read_csv("df_concat_20230712.csv")
        df_2023_07.rename(columns={"index":"Data ID", "Latitude":"lat", "Longitude":"lon"}, inplace=True)
        df_2023_07.drop(columns=["Unnamed: 0.1", "Unnamed: 0"], inplace=True)
        df_2023_07.reset_index(drop=True, inplace=True)
        df_2023_07["Pure Rent"] = df_2023_07["Price"]
        df_2023_07["Dataframe Date"] = "20230712"

        df_timeline = pd.concat([df_2023_05, df_2023_06, df_2023_07])
        st.write(df_timeline)
        st.write(f"Number of records:{len(df_timeline)}")
        st.subheader("Timeline pivoting and aggregating")

        df_timeline_pivotedby_dataframedate = df_timeline.pivot_table(index="Dataframe Date", aggfunc={"Pure Rent":["mean","sum"], "Size":["mean","sum"]}).reset_index()
        df_timeline_pivotedby_dataframedate.columns = [''.join(col).strip() for col in df_timeline_pivotedby_dataframedate.columns.values]
        st.write(df_timeline_pivotedby_dataframedate)

        col1, col2, col3, col4 = st.columns([0.25, 0.25, 0.25, 0.25])
        with col1:

            chart = alt.Chart(df_timeline_pivotedby_dataframedate).mark_line(
                color="red"
            ).encode(
                x='Dataframe Date:O',
                y=alt.Y('Pure Rentmean:Q'),
            ).interactive()

            chart2 = alt.Chart(df_timeline_pivotedby_dataframedate).mark_bar(
                color="#95B5C3",
                opacity=0.5,
            ).encode(
                x='Dataframe Date:O',
                y=alt.Y('Pure Rentmean:Q'),
            ).interactive()


            chart = (chart + chart2)
            chart = chart.encode(alt.Y(title="Average Pure Rent"))
            st.altair_chart(chart, use_container_width=True)

        with col2:

            chart = alt.Chart(df_timeline_pivotedby_dataframedate).mark_line(
                color="red"
            ).encode(
                x='Dataframe Date:O',
                y=alt.Y('Pure Rentsum:Q'),
            ).interactive()

            chart2 = alt.Chart(df_timeline_pivotedby_dataframedate).mark_bar(
                color="#95B5C3",
                opacity=0.5,
            ).encode(
                x='Dataframe Date:O',
                y=alt.Y('Pure Rentsum:Q'),
            ).interactive()


            chart = (chart + chart2)
            chart = chart.encode(alt.Y(title="Total Scraped Rent"))
            st.altair_chart(chart, use_container_width=True)

        with col3:

            chart = alt.Chart(df_timeline_pivotedby_dataframedate).mark_line(
                color="red"
            ).encode(
                x='Dataframe Date:O',
                y=alt.Y('Sizemean:Q'),
            ).interactive()

            chart2 = alt.Chart(df_timeline_pivotedby_dataframedate).mark_bar(
                color="#95B5C3",
                opacity=0.5,
            ).encode(
                x='Dataframe Date:O',
                y=alt.Y('Sizemean:Q'),
            ).interactive()


            chart = (chart + chart2)
            chart = chart.encode(alt.Y(title="Average SQM"))
            st.altair_chart(chart, use_container_width=True)
        with col4:
            chart = alt.Chart(df_timeline_pivotedby_dataframedate).mark_line(
                color="red"
            ).encode(
                x='Dataframe Date:O',
                y=alt.Y('Sizesum:Q'),
            ).interactive()

            chart2 = alt.Chart(df_timeline_pivotedby_dataframedate).mark_bar(
                color="#95B5C3",
                opacity=0.5,
            ).encode(
                x='Dataframe Date:O',
                y=alt.Y('Sizesum:Q'),
            ).interactive()


            chart = (chart + chart2)
            chart = chart.encode(alt.Y(title="Total SQM"))
            st.altair_chart(chart, use_container_width=True)

        #Create a button
        st.markdown("""---""")
        st.markdown("<p style='text-align: center; color: red;'>Send in an email!</p>", unsafe_allow_html=True)
        col1, col2 = st.columns([0.5,0.5])
        with col1:
            email_input = st.text_input('Enter an email', '')
            st.write('The current email is', email_input)
        with col2:
            st.markdown("<p style='text-align: center; color: red;'>Click the button!</p>", unsafe_allow_html=True)

            if st.button("Send email", use_container_width=True):
                button_pressed_2 = True
                st.write("Button pressed!")
                def sendemail():

                    from_addr = st.secrets.email_address
                    password = st.secrets.gmailpassword

                    review = [email_input]

                    # Create MIMEMultipart object
                    msg = MIMEMultipart("application", "octet-stream")
                    msg["Subject"] = "Monthly Real Estate Report - End of March 2023"
                    msg["From"] = from_addr
                    # msg["To"] = to_addr
                    msg["To"] = ", ".join(review)

                    text = MIMEText(
                        '''
                        <html>
                            <head>
                            <title>ELT Real Estate Report</title>
                            <style>
                            
                            body {background-color: #FFFFFF;}
                            
                            .mainDiv {
                                box-shadow: 0;          
                            }
                            
                            </style>
                            </head> 
                            <body>
                            <div class="mainDiv">
                                <div class="myDiv"> 
                                <br>
                                <p style="font-style: italic; font-size: 12px;">Please open full screen on a desktop or laptop.</p>
                                </div>
                            </div>
                            </body> 
                        </html>
                        ''', 'html', 'utf-8')

                    msg.attach(text)


                    file = "Case Study_Asset Management.xlsx"
                    fp = open(file, 'rb')
                    part = MIMEBase('application', 'vnd.ms-excel')
                    part.set_payload(fp.read())
                    fp.close()
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment', filename=file)
                    msg.attach(part)

                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                        server.login(from_addr, password)
                        server.sendmail(from_addr, review, msg.as_string())
                        st.text(f"Email has been sent to {email_input}")
                sendemail()

                def sendslack():
                    # Eliminate the need to check for ssl
                    ssl._create_default_https_context = ssl._create_unverified_context
                    #Create a slack client and define todays date or moment date
                    client = slack.WebClient(token=st.secrets.slack_bot_token)

                    #Tell the client to select a channel and include the specified text.
                    client.chat_postMessage(channel='#special-projects', text="Someone pressed the button on https://christianheins-wggesucht-wggesucht-2lmx07.streamlit.app")
                    print("Sending slack message")
                sendslack()

                button_pressed_2 = False

                if button_pressed_2:
                    st.write("Processing...")
                else:
                    st.write("Ready to refresh again!")
                col1, col2 = st.columns([0.5,0.5])
                with col1:
                    st.image('https://media.giphy.com/media/XathaB5ILqSME/giphy.gif?cid=ecf05e479myrqtfsmnw3tsf81zg8em7pdz1ykm97adrjzwxu&rid=giphy.gif&ct=g', use_column_width=True)
                with col2:
                    st.image('https://media.giphy.com/media/XathaB5ILqSME/giphy.gif?cid=ecf05e479myrqtfsmnw3tsf81zg8em7pdz1ykm97adrjzwxu&rid=giphy.gif&ct=g', use_column_width=True)


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
    #Pages
    page_real_estate_general_dashboard = "wggesucht.py"
    page_maps = "pages/maps.py"

    show_pages(
        [
            Page(page_real_estate_general_dashboard, "General Dashboard", "🏠"),
            Page(page_maps, "Maps", "🗺️"),
        ]
    )

if __name__ == "__main__":
    main()
