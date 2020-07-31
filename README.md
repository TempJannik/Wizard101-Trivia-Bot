# Wizard101-Trivia-Bot

# UPDATE AUGUST 1ST 2020
I did not plan to update the bot, but seeing as how people are charging others for a bot that has a built in captcha solver I decided to update mine.
Shout out to the guy who recommended me the specific captcha solving service (I closed your DM and dont remember your name, if you dm me again I can add credits)

# Changes with the captcha
The usage of this bot is now **no longer free**. To get around the captchas you will have to spend money on a captcha solving service. This bot is configured to work
with https://capmonster.cloud/ . To use this bot, create an account on capmonster, load up funds onto your account ($2 is the minimum) and set your API Key in the config.txt file.

Capmonster charges $0.6 per 1000 Captchas. That means in theory $0.6 for 1000 Trivias or 10000 Crowns. Due to their error rate however you can assume the total
will be more around $0.8-$1.0 per 1000 Captchas. 

Recaptchas also take longer to solve, it can be anywhere from a couple seconds to three minutes for each. Keep this in mind.

**I will not take responsibility for any investment you make, spend money at your own risk!**


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
- Solve Recaptchas
- Switch/Log in to Accounts
- Solve Trivias on multiple accounts at the same time
- Run "invisible" in background

## Config Guide
After the bot starts for the first time it will generate a **config.txt** file. Open it with any texteditor to change your settings.
Available settings:
- **threads**: This is the amount of parallel accounts the bot will do trivia on. Default is 1, I recommend not to go over 2 as you might experience more Too Many Request errors.
- **headless**: This mode, if turned on, will make chrome run in the background. You will not see any chrome tabs, you only have the console output. To turn it on set to 1, set back to 0 to see the tabs again.
- **smartwait**: This is an evasion method for the Too many requests error. Most of the time used by the bot is waiting for captchas to complete. So the most request-intensive action, the answering of questions will be limited to 1 thread at a time. When that thread is done and waiting for a captcha solve the next thread will continue. 
- **tooManyRequestsCooldown**: The amount of seconds to wait after receiving the "Too Many Requests" error. Default is 45 seconds.
- **totalCrownsEarned**: The total amount of crowns this bot has earned you. This will update everytime an account completes its trivias and will persist across multiple uses of the bot.
- **answerDelay**: The amount of seconds to wait before answering each question in a trivia. This can help prevent "Too Many Requests" errors. Default is set to 0.0 seconds
- **tesseractPath**: The Path to your tesseract installation. If you did not install it to "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" like me please change it to your installation path here.

Restart the bot for the changes to take effect.

## Installation without Python
1. Download the release.zip from the [Releases section](https://github.com/TempJannik/Wizard101-Trivia-Bot/releases) and extract the contents into a new folder.
2. Chromedriver - I have supplied my chromedriver in this repository, however you may need to get another version depending on what version of Chrome you have.
If the supplied does not work please do the following:
- First, find out which version of Chrome you are using. Let's say you have Chrome 72.0.3626.81, you can do this in your Settings -> About Chrome.
- Take the Chrome version number, remove the last part, and append the result to URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_". For example, with Chrome version 72.0.3626.81, you'd get a URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_72.0.3626".
- Use the URL created in the last step to retrieve a small file containing the version of ChromeDriver to use. For example, the above URL will get your a file containing "72.0.3626.69". (The actual number may change in the future, of course.)
- Use the version number retrieved from the previous step to construct the URL to download ChromeDriver. With version 72.0.3626.69, the URL would be "https://chromedriver.storage.googleapis.com/index.html?path=72.0.3626.69/".
- Download the chromedriver_win32.zip and extract it into the project folder.

## Usage without Python
1. Open accounts.txt and enter your account information in **username:password** format, one account per line
2. Configure your config.txt
3. Start the bot with by **double clicking TriviaBot.exe**
4. ???
5. Profit

## Installation with Python
1. Download the repository by clicking on the green Clone or Download button on the Top Right, then click Download as ZIP.
2. Extract the ZIP to any location on your PC.
3. Python 3.6.4 - **Make sure to Check the "Add to PATH" box in the installation!** Other versions might work as well but this is the version developement was made on. https://www.python.org/downloads/release/python-364/
4. Open cmd (Type Command Prompt in the windows search) and type **cd "YOUR PROJECT PATH HERE"** for example **cd "C:\Users\Jannik\source\repos\TriviaBot"**
5. Now type **pip install -r requirements.txt**
6. Chromedriver - I have supplied my chromedriver in this repository, however you may need to get another version depending on what version of Chrome you have.
If the supplied does not work please do the following:
- First, find out which version of Chrome you are using. Let's say you have Chrome 72.0.3626.81, you can do this in your Settings -> About Chrome.
- Take the Chrome version number, remove the last part, and append the result to URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_". For example, with Chrome version 72.0.3626.81, you'd get a URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_72.0.3626".
- Use the URL created in the last step to retrieve a small file containing the version of ChromeDriver to use. For example, the above URL will get your a file containing "72.0.3626.69". (The actual number may change in the future, of course.)
- Use the version number retrieved from the previous step to construct the URL to download ChromeDriver. With version 72.0.3626.69, the URL would be "https://chromedriver.storage.googleapis.com/index.html?path=72.0.3626.69/".
- Download the chromedriver_win32.zip and extract it into the project folder.

## Usage with Python
1. Open accounts.txt and enter your account information in **username:password** format, one account per line
2. Configure your config.txt
3. Open cmd (Type Command Prompt in the windows search) and type **cd "YOUR PROJECT PATH HERE"** for example **cd "C:\Users\Jannik\source\repos\TriviaBot"**
4. Start the bot with **python TriviaBot.py**
5. ???
6. Profit

## Changelog
- May 26th 2020: Added Timestamps (thanks for the suggestion AvengerSpencer#9825), fixed a bug causing captchas to error out, better error handling
- May 20th 2020: Fixed a variety of bugs/instabilities, accounts will restart instead of skipping on error, account queue implemented, preventing downtime on threads, config migration
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
- Any Contributors on Github and submitters of bugs 
