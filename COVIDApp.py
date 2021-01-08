from tkinter import *
import requests
import json

# Outputs the number of cases, deaths, and recoveries
def get_data():
    # Gather data from URL
    data_label.configure(font=("Verdana", 18), anchor='center', justify='left')
    country = country_entry.get()
    url = 'https://api.covid19api.com/summary'
    response = requests.get(url)
    data = response.json()
    data = json.loads(response.text)  # deserializes the response object

    # Outputs the global information if user enter "Global"
    if country.lower() == "global":
        data_output = ""
        for key, value in data['Global'].items():
            # Separates the words with a space
            if key[:3] == 'New':
                key = 'New ' + key[3:]
            elif key[:5] == 'Total':
                key = 'Total ' + key[5:]

            # Saves output variable as category and an integer
            data_output += key + ": " + '{:,}'.format(int(value)) + "\n"

        # Determines the date and time
        date = "Date: " + data['Countries'][0]['Date'][:10] + " " + \
               data['Countries'][0]['Date'][11:19] + "\n"

        # Outputs the data on the screen
        data_label['text'] = date + data_output

    # Outputs data of a given country if user enters a country
    else:
        found = False  # Tells whether the given country is found in the dictionary
        should_print = False  # Tells whether the information should be printed
        data_output = "" # String to store information

        # Iterates through the dictionaries under 'Countries'
        for country_data in data['Countries']:

            # Print information if the country is found
            if country in country_data.values():
                for key, value in country_data.items():
                    # Starts printing data if key is 'NewConfirmed'
                    if key == 'NewConfirmed':
                        should_print = True

                    # Stops printing data if key is 'Date'
                    elif key == "Date":
                        should_print = False

                    # Outputs the data on the screen
                    if should_print:
                        # Separates the words with a space
                        if key[:3] == 'New':
                            key = 'New ' + key[3:]
                        elif key[:5] == 'Total':
                            key = 'Total ' + key[5:]

                        # Saves output variable as category and integer
                        data_output += key + ": " + '{:,}'.format(int(value)) + "\n"

                # Determines the date and time
                date = "Date: " + country_data['Date'][:10] + " " + \
                       country_data['Date'][11:19] + "\n"

                # Outputs information on screen
                data_label['text'] = date + data_output

                # Tells program that the country has been found
                found = True
                break

        # Prints a message if the country is not found
        if not found:
            data_label.configure(font=("Verdana", 20, "bold"), anchor='center',
                                 justify='center')
            data_label['text'] = "Country not found."


# Create window and background
window = Tk()
window.title('COVID-19 Tracker')
canvas = Canvas(window, height=600, width=600)
canvas.pack()

# Makes background from an image
background_image = PhotoImage(file='coronavirus-blue.png')
background_label = Label(window, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Create frame to hold title
title_frame = Frame(window, bg='lightgrey', bd=5)
title_frame.place(relx=0.5, rely=0.05, anchor='n')

title = Label(title_frame, text='COVID-19 Tracker', fg='cornflowerblue',
              font=("Times New Roman", 40))
title.pack()
# title.place(relwidth=.5, relheight=1)

# Create frame for entry and button
entry_frame = Frame(window, bg='lightgrey', bd=5)
entry_frame.place(relx=0.5, rely=0.2, relwidth=0.8, relheight=0.1, anchor='n')

country_entry = Entry(entry_frame, text='Enter a country', font=("Verdana", 16))
country_entry.place(relwidth=0.7, relheight=1)

get_data = Button(entry_frame, text='Get Data', font=('Verdana', 14),
                  command=get_data)
get_data.place(relx=0.75, relwidth=0.25, relheight=1)

# Create frame to display data
data_frame = Frame(window, bg='lightgrey', bd=10)
data_frame.place(relx=0.5, rely=0.35, relwidth=0.8, relheight=0.5, anchor='n')

data_label = Label(data_frame, text='Enter a country or "Global" to get worldwide data',
                   font=("Verdana", 16, 'bold'))
data_label.place(relwidth=1, relheight=1)

window.mainloop()
