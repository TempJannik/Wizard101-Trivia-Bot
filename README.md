# Wizard101-Trivia-Bot

## Introduction
I've seen implementations of these type of bots but I've seen none that allow account switching as well which is why I made this Bot.
This will allow you to supply your accounts and have them automatically go through the needed quizzes.

To use this you have 2 choices, with or without Python. Using python is better for more technically experienced people and others who want to know whats being run on their PC. For everyone else I supplied a release in the form of a .exe file.

- [Installation without Python](https://github.com/TempJannik/Wizard101-Trivia-Bot#installation-without-python)
- [Usage without Python](https://github.com/TempJannik/Wizard101-Trivia-Bot#usage-without-python)
- [Installation with Python](https://github.com/TempJannik/Wizard101-Trivia-Bot#installation-with-python)
- [Usage with Python](https://github.com/TempJannik/Wizard101-Trivia-Bot#installation-with-python)
- [Changelog](https://github.com/TempJannik/Wizard101-Trivia-Bot#changelog)
- [Credits](https://github.com/TempJannik/Wizard101-Trivia-Bot#credits)

## Features
- Solve Trivia
- Solve Captcha
- Switch/Log in to Accounts
- Solve Trivias on multiple accounts at the same time
- Run "invisible" in background

## Installation without Python
1. Download the release.rar from the [Releases section](https://github.com/TempJannik/Wizard101-Trivia-Bot/releases) and unpack in into a new folder.
2. Tesseract 5 - **Make sure to install it under C:\Program Files\Tesseract-OCR** https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe
3. Chromedriver - I have supplied my chromedriver in this repository, however you may need to get another version depending on what version of Chrome you have.
If the supplied does not work please do the following:
- First, find out which version of Chrome you are using. Let's say you have Chrome 72.0.3626.81, you can do this in your Settings -> About Chrome.
- Take the Chrome version number, remove the last part, and append the result to URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_". For example, with Chrome version 72.0.3626.81, you'd get a URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_72.0.3626".
- Use the URL created in the last step to retrieve a small file containing the version of ChromeDriver to use. For example, the above URL will get your a file containing "72.0.3626.69". (The actual number may change in the future, of course.)
- Use the version number retrieved from the previous step to construct the URL to download ChromeDriver. With version 72.0.3626.69, the URL would be "https://chromedriver.storage.googleapis.com/index.html?path=72.0.3626.69/".
- Download the chromedriver_win32.zip and extract it into the project folder.

## Usage without Python
1. Open accounts.txt and enter your account information in **username:password** format, one account per line
2. Start the bot with by **double clicking TriviaBot.exe**
3. ???
4. Profit

## Installation with Python
1. Download the repository by clicking on the green Clone or Download button on the Top Right, then click Download as ZIP.
2. Extract the ZIP to any location on your PC.
3. Python 3.6.4 - **Make sure to Check the "Add to PATH" box in the installation!** Other versions might work as well but this is the version developement was made on. https://www.python.org/downloads/release/python-364/
4. Open cmd (Type Command Prompt in the windows search) and type **cd "YOUR PROJECT PATH HERE"** for example **cd "C:\Users\Jannik\source\repos\TriviaBot"**
5. Now type **pip install -r requirements.txt**
6. Tesseract 5 - **Make sure to install it under C:\Program Files\Tesseract-OCR** https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe
7. Chromedriver - I have supplied my chromedriver in this repository, however you may need to get another version depending on what version of Chrome you have.
If the supplied does not work please do the following:
- First, find out which version of Chrome you are using. Let's say you have Chrome 72.0.3626.81, you can do this in your Settings -> About Chrome.
- Take the Chrome version number, remove the last part, and append the result to URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_". For example, with Chrome version 72.0.3626.81, you'd get a URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_72.0.3626".
- Use the URL created in the last step to retrieve a small file containing the version of ChromeDriver to use. For example, the above URL will get your a file containing "72.0.3626.69". (The actual number may change in the future, of course.)
- Use the version number retrieved from the previous step to construct the URL to download ChromeDriver. With version 72.0.3626.69, the URL would be "https://chromedriver.storage.googleapis.com/index.html?path=72.0.3626.69/".
- Download the chromedriver_win32.zip and extract it into the project folder.

## Usage with Python
1. Open accounts.txt and enter your account information in **username:password** format, one account per line
2. Open cmd (Type Command Prompt in the windows search) and type **cd "YOUR PROJECT PATH HERE"** for example **cd "C:\Users\Jannik\source\repos\TriviaBot"**
3. Start the bot with **python TriviaBot.py**
4. ???
5. Profit

## Changelog
- May 15th 2020: Added proper Config file, crowns tracking
- May 14th 2020: Retry failed quizzes (Thanks @zisop16)
- May 13th 2020: Headless mode, stability improvements
- May 11th 2020: Multithreading support
- May 10th 2020: Removed Selenium logging, fixed bug, captcha retry limit
- May 8th 2020: Login stablility, better chrome clean up
- May 6th 2020: Fix Captcha bugs, exception handling, quiz throttle handling and version checking
- May 5th 2020: Initial Release

## Credits
- [The Daily Crown Quiz Answering Extension](https://chrome.google.com/webstore/detail/daily-crown-quiz-answerin/aihenldiapgpgknjngnabfnjdjjffljp) - Looking at it helped me understand the captchas better and some javascript handling.
- Zenmaster#6969 - Helping out with testing and formatting Questions/Answers
- ToxOver#9831 - Me
