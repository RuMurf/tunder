<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href='#the-algorithm'>The Algorithm</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <ul>
          <li><a href='#optional-prerequisites'>Optional Prerequisites</a></li>
        </ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://github.com/RuMurf/tunder)

For my undergraduate final year project I was tasked with researching and developing a music recognition application (similar existing applications such as Shazam and Musicxmatch). This is the resulting application.

After experimenting with different Machine Learning and Information Retrieval methods I decided to follow a similar aproach to the original [Shazam algorithm][Shazam-paper].

### The Algorithm

The algorithm uses audio "fingerprints" to identify clips of music in the presence of noise (as there would be in a sample recorded through an end user device's microphone). Each track in the database is run through this fingerprinting process and the fingerprint is what is saved to the database. These fingerprints contain the most important identifying information of a track in a very compact form, allowing for smaller databases and faster matching.

The matching process is very similar to that of human fingerprint matching. The sample clip is run through the same fingerprinting process and the resuting fingerprint is matched againts all the fingerprints in the database. There will be some false matches and not all points on the sample fingerprint will match the correct track. However, this process works on the basis that a vast majority of points will match, at a given time position, on the original track over other tracks in the database.


<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [![Python][Python.org]][Python-url]
* [![NodeJS][NodeJS]][NodeJS-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

The following instructions are based on the presumtion that you are on Windows and using cmd. The process is vwery similar for Linux/Bash users.

### Prerequisites

* The latest version of [Python][Python-url]
* The latest version of [Node.js][NodeJS-url] and npm

#### Optional Prerequisites

* [ffmpeg][ffmpeg-url]
  * madmom only works natively with audio recorded at 44100Hz. It can work with audio recorded at other sample rates but it needs ffmpeg to convert them.
  * It is recomended that ffmpeg is installed and added to the system's path for optimal compatibility

### Installation

1. Clone the repo
   ```sh
   git clone https://https://github.com/RuMurf/tunder.git
   ```
2. Install NPM packages
   ```sh
   npm install
   ```
3. Install dependencies for Python application:
    * Madmom, one of the main modules used for spectral analysis, doesn't automatically install it's own dependencies. As such, if it is installed the standard way (via requirements.txt) it will throw an error and abort the entire process. I wrote a simple workaround batch file which installs the dependencies from requirements.txt and then installs madmom from a seperate command.
    * Navigate to "application\" and run: 
    ```sh
    install-dependencies.bat
    ```
    * Make sure to run the batch file from your virtual environment if using one.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

* To start the server run: 
  ```sh
    npm start
  ```
  * This runs the server using nodemon, which monitors the codebase for any changes after the server crashes and automatically restarts the server when a change is detected.

* You can then see the UI by accessing localhost or the machine's private IP address through a web browser.

* Once the "Record" Button is pressed, The browser will record a short clip of audio from the device's microphone and send it to the server in a HTTP request. When the server recieves the request it calls `application\src\match_program.py`, passing the previously recieved audio file as an arguement.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Configuration variables for database connection strings, etc.
- [ ] Support for HTTPS
    - Due to chrome's security features, audio can only be recorded by the browser over a secured HTTPS connection. As a result, this application currently only functions when run on the same machine as the server.
- [ ] Native Android and IOS client applications
- [ ] Investigate machine learning aproaches such as deep neural networks


<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments


* Thanks to [Othneil Drew](https://github.com/othneildrew) for the [README template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: homepage.png
[Shazam-paper]: https://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf

[Python.org]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://python.org
[NodeJS]: https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white
[NodeJS-url]: https://nodejs.org
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[ffmpeg-url]: https://ffmpeg.org