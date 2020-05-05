# Wizard101-Trivia-Bot

## Introduction
I've seen implementations of these type of bots but I've seen none that allow account switching as well which is why I made this Bot.
This will allow you to supply your accounts and have them automatically go through the needed quizzes.

## Installation
1. Python 3.6.4 - **Make sure to Check the "Add to PATH" box in the installation!** Other versions might work as well but this is the version developement was made on. https://www.python.org/downloads/release/python-364/
2. Open cmd (Type Command Prompt in the windows search) and type **cd "YOUR PROJECT PATH HERE"** for example **cd "C:\Users\Jannik\source\repos\TriviaBot"**
3. Now type **pip install -r requirements.txt**
4. Tesseract 5 - **Make sure to install it under C:\Program Files\Tesseract-OCR** https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe
5. Chromedriver - I have supplied my chromedriver in this repository, however you may need to get another version depending on what version of Chrome you have.
If the supplied does not work please do the following:
- First, find out which version of Chrome you are using. Let's say you have Chrome 72.0.3626.81, you can do this in your Settings -> About Chrome.
- Take the Chrome version number, remove the last part, and append the result to URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_". For example, with Chrome version 72.0.3626.81, you'd get a URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_72.0.3626".
- Use the URL created in the last step to retrieve a small file containing the version of ChromeDriver to use. For example, the above URL will get your a file containing "72.0.3626.69". (The actual number may change in the future, of course.)
- Use the version number retrieved from the previous step to construct the URL to download ChromeDriver. With version 72.0.3626.69, the URL would be "https://chromedriver.storage.googleapis.com/index.html?path=72.0.3626.69/".
- Download the chromedriver_win32.zip and extract it into the project folder.

## Usage

1. Open accounts.txt and enter your account information in **username:password** format, one account per line
2. Open cmd (Type Command Prompt in the windows search) and type **cd "YOUR PROJECT PATH HERE"** for example **cd "C:\Users\Jannik\source\repos\TriviaBot"**
3. Start the bot with **python TriviaBot.py**
4. ???
5. Profit

## Credits
- [The Daily Crown Quiz Answering Extension](https://chrome.google.com/webstore/detail/daily-crown-quiz-answerin/aihenldiapgpgknjngnabfnjdjjffljp) - Looking at it helped me understand the captchas better and some javascript handling.
- Zenmaster#6969 - Helping out with testing and formatting Questions/Answers
- ToxOver#9831 - Me
