# COVID-19 Data Visualizer
A simple and fast Qt-based GUI for visualzing COVID-19 data

# Update :
**This project is outdated and not maintained.**

## Installation
1. Python(3.8.5)  must be installed and added to PATH. 
2. The program uses the following libraries. These must be installed:
    * pyqt5
    * pyqtgraph
    * pandas
    * numpy
    * requests
    * json
    * urllib
    * speech-recognition
    * sounddevice
    * random
    * datetime
    * scipy
   
   Not really recommended, but if you want to : Alternatively, you can skip this step and run install_covid_tracker_dependencies.py to install the dependencies by opening a terminal and running : `python install_covid_tracker_dependencies.py`. This will install all the required libraries using pip package manager. Make sure pip is on PATH.
  
3. For Linux based OS, you also might have to run this in a terminal (This is requred by sounddevice module.).

   `sudo apt-get install libportaudio2`
   
    If that didn't work, try this :
	
   `sudo apt-get install libasound-dev`


4. After this you can run the main program by opening a terminal and running : `python covid-19-tracker-qt.py`
    
## Usage
This is the window at the start of the program.

![Start Window Image](https://github.com/davistdaniel/covid-19-tracker/blob/master/screenshots/Annotation%202020-09-08%20203434.png)
The program detects your the country you are in, based on your IP address.It plots the current cases data for your country. The location is obtained from [here](https://geolocation-db.com/json).

**Of course,you can switch this feature off easily before running the program by removing the code statement on line 174 : `self.start_covid()`**. 

The data is obtained from Covid-19 data provided by the [European Centre for Disease Prevention and Control](https://opendata.ecdc.europa.eu/covid19/casedistribution/csv). The data is updated daily and contains the latest available public data on the number of new Covid-19 cases reported per day and per country.

The plotting is done with [`pyqtgraph`](http://www.pyqtgraph.org/) which is fast with the graphics and works well while being embedded in a Qt application.

Three different parameters can be visualized per country:
* Infections
* Deaths
* Cumulative average of 14 days per 100000 people.

#### Dark-Light combo box
This combox box lets you choose the theme of the GUI. Depending on the time given by the machine your are running the program on. If you open the program between 7:00 and 19:00, the theme is light. For all other times, the theme is set to dark.

#### Plot-type combo box
This combox box lets you choose the paramter you want to plot.
Three different paramters can be visualized per country:
* Infections
* Deaths
* Cumulative average of 14 days per 100000 people
* Comparison

#### Country Name
The name of the country you want the data to be visualzed for can be given in the text box to the top of the **Track!** button. The country name must start with a the first letter capital. For countries wiht names having multiple words, name should be given accordingly. For e.g, USA should be given as United States of America or for UK, it must be given as United Kingdom. If the country name is 'None selected' or or the country name is misspelt, a random country is selected and the data is visualized.You can have a look at the 'History log' text box to see history of your interaction with the the program. The 'Data' table towards the left of the text box shows the data for the selected country.

#### The `Track!` button.
After selecting a parameter to be plot and typing in the country you want to plot, click on Track! button to visualize the data.  

#### The plotting tab.
The plotting tab consists of two tabs. **Plot 1** shows the current graph while **Plot 2** tab shows a comparison of all the data which was visualized until now. This is useful when you want compare data between multiple countries. Note that pressing 'Reset!' button clears both plots tabs.

#### Animate checkbox
As the name suggests, checking on animate checkbox will animate the plots. Any data you visualize would show how the parameter you selected progressed over the days for the selected country.
![Animated plot](https://github.com/davistdaniel/covid-19-tracker/blob/master/screenshots/animated_plot.gif)

#### The `Speak!` button.
This is an experimental feature and may not always work. When you click on the button, the program listens for 5 seconds. You can give the following commands:
* Dark : Switch to Dark them.
* Light : Switch to Light theme.
* Infections : Change plot type to 'infections'
* Deaths : Change plot type to 'deaths'
* Cumulative : Change plot type to 'Cumulative Average'
* Reset : Reset the program.
* Animated : Activate the 'Animated' checkbox.
* Track :  Clicks on the track buttton to plot the data for the country selected.

**You can also speak any country's name after clicking the button and the data will be plotted automatically.**

Note : The transcription service is from Google. It fails occasionaly. An error message is printed in the history log text box if this happens. 


Here's a quick recap of everything so far:

![All functions shown](https://github.com/davistdaniel/covid-19-tracker/blob/master/screenshots/full_gif.gif)
