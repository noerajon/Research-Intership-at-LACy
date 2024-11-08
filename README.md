My name is Noé Rajon, I did an intership at the LACy laboratory at La Réunion. During this intership I developed a specific filter to classify aerosols at La Réunion.
If you are interested in having an overview of the current aerosols type at la Réunion, please read carefully the rules below:

1. Download the repository "Research-Intership-at-LACy" and unzip it.
2. Downloading the AERONET data on the AERONET website (https://aeronet.gsfc.nasa.gov/)

   --> click on +Data Display under the AEROSOL OPTICAL DEPTH (V3)-SOLAR panel
   
   --> Zoom with the mouse wheel on the map near Reunion Island and click on the (20.9S, 55.5E) point and click on REUNION_ST_DENIS

   --> Under the AERONET DOWNLOAD panel click on "More AERONET Downloadable Products..."

   --> Select your time span using the "START" and "END" boxes

   --> Select the "Level 2.0" of the "Aerosol Optical Depth (AOD) with Precipitable Water and Angstrom Parameter"

   --> Check that "All Points" are ticked in the "Data Format"

   --> Click on the "Download" button and wait.

   --> A new window will appear and click on "Accept"

4. Preparing the data

--> Unzip the file that you just downloaded and go through the folder until you find the file with the LEV20 extension

--> Place this file in the "Research-Intership-at-LACy-main\Research-Intership-at-LACy-main\data\BRUT\AERONET\CURRENT" folder

--> Make sure that this is the only file in the folder, if necessary, delete the others.
If there are no files or more than one file an error will be raised when the script will be launched.
You will remark that once you downloaded the repository there is already a file in the corresponding folder, it is just for the example.

5. Aerosol typings

--> With a python interpreter, open the script called "AEROSOL_TYPING_Current_typing" and Run the script.

--> You may have to install some additional libraries, you could do it with the following command

pip install "name of the library"

At the end, you will obtain bar charts representing for two aerosol typings filter, the different type of aerosols in quantities for the time span choosen.
