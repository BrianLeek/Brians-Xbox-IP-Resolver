<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">Brian's Xbox IP Resolver (Gamertag2IP)</h3>

  <p align="center">
    Brian's Xbox IP Resolver is a script created in Python that uses SQLite for the database.  By using SQLite3 you can create new databases that will be stored on you computer rather then on a server elsewhere. By doing this it makes sharing and switching between databases easier when using the script. The script will come with a preexisting database that contains a mass log of IPs, gamertags, etc that can be used to search through right away.
    <br />
    <p align="center">
    <a href="https://brianleek.me/documentation/brians-xbox-ip-resolver/"><strong>Explore the docs »</strong></a>
  </p>
  </p>
</p>

<!-- WHAT IS BRIAN'S XBOX IP RESOLVER -->
## What Is Brian's Xbox IP Resolver
Brian's Xbox IP Resolver (Gamertag2IP) is a script created in Python that will come with a preexisting database so you won't need to create one and add information to it. The main database will receive updates every so often. Since the main database already has information in it you can begin searching right away. You can search for a Xbox users IP Address, XUID, and Machine ID (MID) with just their gamertag from the main database if available. The script also allows users to create their own databases too! You can contribute to the main overall database by submitting your database to the developer to be merged together or they can share their database online for others online to use.

The main database is created on the developers side which works by using the IP log (iplog.txt) file generated by ApparitionNET when logging IPs, other ways to import from a ip log file are planned. Once the file is created it is dropped into the scripts root and the script uses that to create or add that information to a new/existing database. Data can also be entered manually as well if needed. 

<!-- INSTALLING THE SCRIPT -->
## Installing The Script

Installing Brian's Xbox IP Resolver is very easy to do. Once you downloaded the script make sure you have the latest version of Python installed before continuing. Open CMD/Terminal and go to the scripts root folder and run the following command to install all the needed requirements:

`pip install -r requirements.txt`

It's recommended you create a virtual environment before installing a requirements.txt file. Anyways after you installed the needed requirements all you need to do now is run the script and your good to go. To run the script run this command:

`python main.py`

<!-- CHANGELOG -->
## Changelog

### 0.1
 - Initial Release.

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are greatly appreciated.

<!-- CONTACT -->
## Contact

Brian Leek - [@Precutting](https://twitter.com/precutting) - https://brianleek.me/
