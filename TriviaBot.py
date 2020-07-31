import time
import urllib.request
import os
import base64
import colorsys
import sys
import math
import difflib
import pytesseract as tess
from urllib.request import urlopen
from utility_methods.utility_methods import *
from selenium import webdriver
from functools import reduce
from PIL import Image
from PIL import ImageGrab
from pytesseract import Output
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import threading
import json
import queue
import io
import requests
from datetime import datetime

version = "13"
totalCrownsEarned = 0
headless = False
tooManyRequestsCooldown = 45
answerDelay = 0.0
captchasRequest = 0
captchasFailed = 0
accountQueue = queue.Queue()
lock = threading.Lock()

def isVersionOutdated():
    newestVersion = urlopen("https://raw.githubusercontent.com/TempJannik/Wizard101-Trivia-Bot/master/version.txt").read().decode('utf-8')
    if newestVersion != version:
        print("Your Bot seems to be outdated. Please visit https://github.com/TempJannik/Wizard101-Trivia-Bot for the newest version. Download the newest release and replace the files in your bots folder.")
        input("Press enter to continue with the old version...")

def printTS(message):
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S")
    print("["+dt_string+"] " + message)
    lock.acquire() # Aquire lock to prevent other threads opening the file while its being messed with
    path = os.path.dirname(os.path.realpath(__file__))
    with open(path+'/log.txt', 'a') as f:
        f.write("\n["+dt_string+"] " + message)
    lock.release()

switcherMagical = {
                "Zafaria is home to what cultures?":"Gorillas, Zebras, Lions",
                "Which of these locations is not in Wizard City?":"Digmore Station",
                "What book does Professor Drake send you to the library to check out?":"Book on the Wumpus",
                "What is the title of the book that is floating around the Wizard City Library?":"Basic Wizarding & Proper Care of Familiars",
                "How many worlds of The Spiral are unlocked as of May 21st, 2014?":"12",
                "Why are the Gobblers so afraid to go home?":"Witches",
                "Merle Ambrose is originally from which world?":"Avalon",
                "Who sells Valentine's Day items in Wizard City?":"Valentina Heartsong",
                "Who is the Registrar of Pigswick Academy?":"Mrs. Dowager",
                "Who guards the entrance to Unicorn Way?":"Private Stillson",
                "What's the name of the balance tree?":"Niles",
                "What can be used to diminish the Nirini's powers in Krokotopia?":"Flame Gems",
                "Why are the pixies and faeries on Unicorn Way evil?":"Rattlebones corrupted them.",
                "Which below are NOT a type of Oni in MooShu?":"Ruby",
                'Who prophesizes this? "The mirror will break, The horn will call, From the shadows I strike , And the skies will fall..."':"Morganthe",
                "Who is the Nameless Knight?":"Sir Malory",
                "What color is the door inside the boys dormroom?":"Red",
                "What is the shape of the pink piece in potion motion?":"Heart",
                "Which one of these are not a symbol on the battle sigil?":"Wand",
                "What did Prospector Zeke lose track of in MooShu?":"Blue Oysters",
                "Which is the only school left standing in Dragonspyre?":"Fire",
            }

switcherAdventuring = {
                "What is Professor Falmea's favorite food?":"Pasta Arrabiata",
                "What hand does Lady Oriel hold her wand in?":"Trick question, she has a sword.",
                "What determines the colors of the manders in Krok?":"Where they come from and their school of focus.",
                "What school is the spell Dark Nova":"Shadow",
                "How long do you have to wait to join a new match after fleeing in PVP?":"5 minutes",
                "Who is in the top level of the Tower of the Helephant?":"Lyon Lorestriker",
                "What type of rank 8 spell is granted to Death students at level 58?":"Damage + DoT",
                "Which of these are not a lore spell?":"Fire Dragon",
                "An unmodified Sun Serpent does what?":"900 � 1000 Fire Damage + 300 Fire Damage to entire team",
                "Which of these is NOT a Zafaria Anchor Stone?":"Rasik Anchor Stone",
                "Who is the Bear King of Grizzleheim?":"Valgard Goldenblade",
                "What is the name of the secret society in Krokotopia":"Order of the Fang",
                "What is unique about Falmea's Classroom?":"There are scorch marks on the ceiling",
                "In Grizzleheim, the Ravens want to bring about:":"The Everwinter, to cover the world in ice:",
                "What is the name of the new dance added with Khrysalis?":"The bee dance",
                "What is the name of the book stolen from the Royal Museum?":"The Krokonomicon",
                "Which Aztecan ponders the Great Questions of Life?":"Philosoraptor",
                "What does the Time Ribbon Protect against?":"Time Flux",
                "What school is the Gurtok Demon focused on?":"Balance",
                "Shaka Zebu is known best as:":"The Greatest Living Zebra Warrior",
            }

switcherConjuring = {
                "Who is Bill Tanner's sister?":"Sarah Tanner",
                "What is the shape on the weather vanes in the Shopping District?":"Half moon/moon",
                "What book was Anna Flameright accused of stealing?":"Advanced Flameology",
                "What level must you be to wear Dragonspyre crafted clothing?":"33",
                "What did Abigail Dolittle accuse Wadsworth of stealing?":"Genuine Imitation Golden Ruby",
                "What was the name of the powerful Grendel Shaman who sealed the runic doors?":"Thulinn",
                "Who Is NOT a member of the Council of Light?":"Cyrus Drake",
                "Sir Edward Halley is the Spiral's most famous:":"Aztecosaurologist",
                "Who is the King of the Burrowers?":"Pyat MourningSword",
                'Which Queen is mentioned in the Marleybone book "The Golden Age"?':"Ellen",
                "How many portal summoning candles are in the Burial Mound?":"Three",
                "Kirby Longspear was once a student of which school of magic?":"Death",
                "The Swordsman Destreza was killed by:":"A Gorgon",
            }

switcherMarleybone = {
                "Arthur Wethersfield is A:..":"Dog",
                "What course did Herold Digmoore study?":"Ancient Myths for Parliament",
                "What is flying around in Regent's Square?":"Newspapers",
                "What time of day is it always in Marleybone?":"Night",
                "What two names are on the Statues in the Marleybone cathedral?":"Saint Bernard and Saint Hubert",
                "What event is Abigail Doolittle sending out invitations for?":"Policeman's Ball",
                "What sort of beverage is served in Air Dales Hideaway?":"Root Beer",
                "What is a very common last name of the cats in Marleybone?":"O'Leary",
                "Who is not an officer you'll find around Marleybone?":"Officer Digmore",
                "What style of artifacts are in the Royal Museum?":"Krokotopian",
                "What initials were on the doctor's glove?":"XX",
                "Who is the dangerous criminal that is locked up, but escapes from Newgate Prison?":"Meowiarty",
                "What color are the Marleybone mailboxes?":"Red",
                "Which of these folks can you find in the Royal Museum?":"Clancy Pembroke",
                "Which is not a street in Regent's Square?":"Fleabitten Ave",
                "What is Sgt. Major Talbot's full name?":"Sylvester Quimby Talbot III",
                "What time does the clock always read in Marleybone?":"1:55",
                "Which symbol is not on the stained glass window in Regent's Square?":"A Tennis Ball",
                "What transports you from place to place in Marleybone?":"Hot Air Balloons",
                "What did Prospector Zeke lose in Marleybone?":"The Stray Cats",
            }

switcherMystical = {
                "Who is the Emperor of Mooshu's Royal Guard?":"Noboru Akitame",
                "In what world would you find the Spider Temple":"Zafaria",
                "Where is the only pure fire in the Spiral found?":"Wizard City",
                "King Neza is Zenzen Seven Star's:?":"Grandfather",
                "What was Ponce de Gibbon looking for in Azteca?":"The Water of Life",
                "In Reagent's Square, the Professor is standing in front of a:":"Telegraph Box",
                "Hrundle Fjord is part of what section of Grizzleheim?":"Wintertusk",
                "King Axaya Knifemoon needs what to unify the people around him?":"The Badge of Leadership",
                "Which villain terrorizes the fair maidens of Marleybone?":"Jaques the Scatcher",
                "Who gives you permission to ride the boat to the Krokosphinx?":"Sergent Major Talbot",
                "Who is the only person who knows how to enter the Tomb of Storms?":"Hetch Al'Dim",
                "Who was ordered to guard the Sword of Kings?":"The Knights of the Silver Rose",
                "Who did Falynn Greensleeves fall in love with?":"Sir Malick de Logres",
                "Who was the greatest Aquilan Gladiator of all time?":"Dimachaerus",
                "Who haunts the Night Warrens?":"Nosferabbit",
                "Who tells you how to get to Aquila?":"Harold Argleston",
                "Who takes you across the River of Souls?":"Charon",
                "Thaddeus Price is the Pigswick Academy Professor of what school?":"Tempest",
                "Who asks you to find Khrysanthemums?":"Eloise Merryweather",
                "What is used to travel to the Isle of Arachnis?":"Ice Archway",
            }

switcherSpellbinding = {
                "Who makes the harpsicord for Shelus?":"Gretta Darkkettle",
                "Morganthe got the Horned Crown from the Spriggan:":"Gisela",
                "Sumner Fieldgold twice asks you to recover what for him?":"Shrubberies",
                "Who needs the healing potion from Master Yip?":"Binh Hoa",
                "Who is Haraku Yip's apprentice?":"Binh Hoa",
                'Who taunts you with: "Prepare to be broken, kid!"':"Clanker",
                "What badge do you earn by defeating 100 Samoorai?":"Yojimbo",
                "Who thinks you are there to take their precious feathers?":"Takeda Kanryu",
                "The Swallows of Caliburn migrate to Avalon from where each year?":"Zafaria and Marleybone",
                'Who tells you: "A shield is just as much a weapon as the sword."':"Mavra Flamewing",
                'Who tells you to speak these words only unto your mentor: "Meena Korio Jajuka!"':"Priya the Dryad",
                "Who tries to raise a Gorgon Army?":"Phorcys",
                'Who taunts you with: "Wizard, you will know the meaning of the word pain after we battle!"':"Aiuchi",
                "What special plant was Barley developing in his Garden?":"Cultivated Woodsmen",
                "Who helps Morganthe find the Horn of Huracan?":"Belloq",
                "Who taunts: Why I oughta knock you to the moon, you pesky little creep!":"Mugsy",
                "What does Silenus name you once you've defeated Hades?":"Glorious Golden Archon",
                "In Azteca, Morganthe enlisted the help of the:":"The Black Sun Necromancers",
                "Where has Pharenor been imprisoned?":"Skythorn Tower",
                "Who grants the first Shadow Magic spell?":"Sophia DarkSide",
            }

switcherSpells = {
                "Mortis can teach you this.":"Tranquilize",
                "What term best fits Sun Magic Spells?":"Enchantment",
                "What type of spells are Ice, Fire, and Storm?":"Elemental",
                "Who can teach you the Life Shield Spell?":"Sabrina Greenstar",
                "Mildred Farseer teaches you what kind of spell?":"Dispels",
                "What term best fits Star Magic Spells?":"Auras",
                "Who teaches you balance magic?":"Alhazred",
                "What isn't a shadow magic spell?":"Ebon Ribbons",
                "Which spell can't be cast while polymorphed as a Gobbler?":"Pie in the sky",
                "If you can cast Storm Trap, Wild Bolt, Catalan, and the Tempest spell, what are you polymorphed as?":"Ptera",
                "How many pips does it cost to cast Stormzilla?":"5",
                "Which spell would not be very effective when going for the elixir vitae Badge?":"Entangle",
                "Cassie the Ponycorn teaches this kind of spell:":"Prism",
                "What level of spell does Enya Firemoon Teach?":"80",
                "If you're a storm wizard with 4 power pips and 3 regular pips, how powerful would your supercharge charm be?":"110%",
                "How many pips does it cost to cast Dr. Von's Monster?":"9",
                "What does Forsaken Banshee do?":"375 damage plus a hex trap",
                "Which Fire spell both damages and heals over time?":"Power Link",
                "Ether Shield protects against what?":"Life and Death attacks",
                "Tish'Mah specializes in spells that mostly affect these:":"Minions",
            }

switcherValencia = {
                "Historian Gonzago is on a stage, who isn't in the audience?":"Giafra",
                'Historian Gonzago sends you on a "Paper Chase," who do you talk to during that quest?':"Magdalena",
                "How many Mechanical Birds do you collect in Sivella?":"5",
                "The Mooshu Tower in Sivella is a replica of what?":"Tower of Serenity",
                "What are Albus and Carbo?":"Armada Commanders",
                "What color of Windstone do you find in Marco Pollo's Tomb?":"Blue",
                "What kind of disguise do you wear in Sivella?":"Clockwork",
                "What shows Steed you're part of the Resistence?":"Amulet",
                "What type of boat do you use to get from the docks to Sivella?":"Gondola",
                "What type of item does Prospector Zeke want you to find in Valencia?":"Birds",
                "What's the name of a librarian in Sivella?":"Grassi",
                "Where do you find the Tomb of Marco Pollo?":"Granchia",
                "Which one isn't a Scholar by name?":"Caresini",
                "Which world doesn't have a pillar in Sivella?":"Monquista",
                "Who do you find in the Lecture Hall of Sivella?":"Ridolfo",
                "Who does Steed send you to speak to in Sivella?":"Thaddeus",
                "Who reads the inscription on Marleybone's Tower?":"Ratbeard",
                "Why does Steed want you to attack Armada Ships?":"Make a Disguise",
                "You need a good eye to save these in Granchia...":"Art Objects",
                "You won't find this kind of Armada Troop in Sivella!":"Battle Angel",
            }

switcherWizard = {
                "Who is the Fire School professor?":"Dalia Falmea",
                "What school does Malorn Ashthorn think is the best?":"Death",
                "What is the name of the bridge in front of the Cave to Nightside?":"Rainbow Bridge",
                "What does every Rotting Fodder in the Dark Caves carry with them?":"A spade",
                "Who is the Wizard City mill foreman?":"Sohomer Sunblade",
                "What is Diego's full name?":"Diego Santiago Quariquez Ramirez the Third",
                "What is something that the Gobblers are NOT stockpiling in Colossus Way?":"Broccoli",
                "Where is Sabrina Greenstar?":"Fairegrounds",
                "Who sang the Dragons, Tritons and Giants into existance?":"Bartleby",
                "What are the school colors of Balance?":"Tan and Maroon",
                "What are the main colors for the Myth School?":"Blue and Gold",
                "What school is all about Creativity?":"Storm",
                "What is the gemstone for Balance?":"Citrine",
                "Who resides in the Hedge Maze?":"Lady Oriel",
                "Who taught Life Magic before Moolinda Wu?":"Sylvia Drake",
                "Who is the Princess of the Seraphs?":"Lady Oriel",
                "What is the name of the school newspaper? Boris Tallstaff knows...":"Ravenwood Bulletin",
                "What is the name of the grandfather tree?":"Bartleby",
                "What is Mindy's last name (she's on Colossus Blvd)?":"Pixiecrown",
                "What is the name of the Ice Tree in Ravenwood?":"Kelvin",
            }

switcherZafaria = {
                "What does Lethu Blunthoof says about Ghostmanes?":"You never can tell with them!",
                "Sir Reginal Baxby's cousin is:":"Mondli Greenhoof",
                "Baobab is governed by:":"A Council of three councilors.",
                "Who is the missing prince?":"Tiziri Silvertusk",
                "Umlilo Sunchaser hired who as a local guide?":"Msizi Redband",
                "Inyanga calls Umlio a:":"Fire feather",
                "The Fire Lion Ravagers are led by:":"Nergal the Burned Lion",
                "Unathi Nightrunner is:":"A councilor of Baobab.",
                "Who is not one of the Zebu Kings:":"Zaffe Zoffer",
                "Rasik Pridefall is:":"An Olyphant from Stone Town.",
                "Esop Thornpaw gives you a magic:":"Djembe Drum",
                "The Inzinzebu Bandits are harassing the good merchants in:":"Baobab Market",
                "Vir Goodheart is an assistant to:":"Rasik Pridefall",
                "Belloq is first found in:":"The Sook",
                "Zebu Blackstripes legendary blade was called:":"The Sword of the Duelist",
                "Jambo means:":"Hello.",
                "Zebu Blackstripes legendary blade was forged:":"In the halls of Valencia",
                "Koyate Ghostmane accuses the player of:":"Being a thief",
                "Who are Hannibal Onetusk's brother and co-pilot?":"Mago and Sobaka",
                "Zamunda's great assassin is known as:":"Karl the Jackal",
            }

class TriviaBot:
    def __init__(self):
        self.login_url = "https://www.wizard101.com/game/"
        self.startChrome()
        self.earnedCrowns = 0
        self.activeAccount = ""
        self.accountsRun = 0

    def startChrome(self):
        global headless
        try:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_argument("--enable-automation")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-browser-side-navigation")
            chrome_options.add_argument("--disable-gpu")
            path = os.path.dirname(os.path.realpath(__file__))
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            self.driver = webdriver.Chrome(path+"/chromedriver.exe", options=chrome_options)
        except:
            printTS("Failed to start Chrome! Your chromedriver version is most likely incompatible. Please see the Github Tutorial on how to get the correct version.")
            input()
            exit()

    def start(self):
        global accountQueue
        while not accountQueue.empty():
            account = accountQueue.get()
            self.doAccount(account)

        print("\n\n")
        printTS("Thread Summary")
        printTS("Earned " + str(self.earnedCrowns)+" crowns on " + str(self.accountsRun) + " accounts.\n")
        self.driver.quit()

    def doAccount(self, account, numAttempts = 1):
        try:
            printTS("Starting login for " +account[0])
            self.login(account[0], account[1])
            self.driver.switch_to.default_content()
            while len(self.driver.find_elements_by_xpath("//*[contains(text(), 'Logout')]")) == 0:
                printTS("Login failed, retrying...")
                self.driver.get("https://www.wizard101.com/auth/logout/freekigames?redirectUrl=https://www.wizard101.com/game/")
                self.login(account[0], account[1])
                time.sleep(2)
            self.activeAccount = account[0]
            self.activeAccountCrowns = 0
            
            self.doQuiz("Magical", "https://www.wizard101.com/quiz/trivia/game/wizard101-magical-trivia")
            self.doQuiz("Adventuring", "https://www.wizard101.com/quiz/trivia/game/wizard101-adventuring-trivia")
            self.doQuiz("Conjuring", "https://www.wizard101.com/quiz/trivia/game/wizard101-conjuring-trivia")
            self.doQuiz("Marleybone", "https://www.wizard101.com/quiz/trivia/game/wizard101-marleybone-trivia")
            self.doQuiz("Mystical", "https://www.wizard101.com/quiz/trivia/game/wizard101-mystical-trivia")
            self.doQuiz("Spellbinding", "https://www.wizard101.com/quiz/trivia/game/wizard101-spellbinding-trivia")
            self.doQuiz("Spells", "https://www.wizard101.com/quiz/trivia/game/wizard101-spells-trivia")
            self.doQuiz("Valencia", "https://www.wizard101.com/quiz/trivia/game/pirate101-valencia-trivia")
            self.doQuiz("Wizard", "https://www.wizard101.com/quiz/trivia/game/wizard101-wizard-city-trivia")
            self.doQuiz("Zafaria", "https://www.wizard101.com/quiz/trivia/game/wizard101-zafaria-trivia")
            printTS("Earned a total of " + str(self.activeAccountCrowns) + " crowns on account: " + self.activeAccount)
            updateTotalEarned(self.activeAccountCrowns)
            self.accountsRun = self.accountsRun + 1
            self.driver.get("https://www.wizard101.com/auth/logout/freekigames?redirectUrl=https://www.wizard101.com/game/")
        except Exception as e:
            self.driver.quit()
            self.startChrome()
            if numAttempts == 3:
                printTS("Following Exception occured while trying to complete this account "+account[0]+ ". Skipping account.\n"+str(e))
                return
            else:
                printTS("Following Exception occured while trying to complete this account "+account[0]+ ". Restarting account.\n"+str(e))
                self.doAccount(account, numAttempts = numAttempts+1)

    def doQuiz(self, quizName, quizUrl, numAttempts = 1):
        global totalCrownsEarned
        global tooManyRequestsCooldown
        global answerDelay
        try:
            self.driver.get(quizUrl)
            WebDriverWait(self.driver,10).until(lambda driver: self.driver.find_elements(By.XPATH,"//*[contains(text(), 'Trivia')]")) # I noticed if the internet sucks or the page bugs out, when switching triiva the result is a blank blue page, this ensures the page loaded properly and if not raise an exception forcing a reload
            while len(self.driver.find_elements_by_xpath("//*[contains(text(), 'YOU PASSED THE')]")) == 0 and len(self.driver.find_elements_by_xpath("//*[contains(text(), 'YOU FINISHED THE')]")) == 0:
                #printTS("Not finished, sleeping...")
                if len(self.driver.find_elements_by_xpath("//*[contains(text(), 'Too Many Requests')]")) != 0: #Error 429 handling
                    printTS("Too many requests, waiting "+str(tooManyRequestsCooldown)+" seconds for a retry. If this occurs often please increase the delay in the settings or decrease the amount of threads.")
                    time.sleep(tooManyRequestsCooldown)
                    self.doQuiz(quizName, quizUrl)
                    return
                if len(self.driver.find_elements_by_xpath("//*[contains(text(), 'Come Back Tomorrow!')]")) != 0: #Quiz throttle handling
                    printTS("Quiz throttled, skipping quiz.")
                    return
                while len(self.driver.find_elements_by_class_name("quizQuestion")) == 0:
                    time.sleep(0.01)
                self.driver.execute_script("""for (let index = 0; index < 4; index++) { document.getElementsByClassName('answer')[index].style.visibility = "visible"; }""")
                question = ""
                while question == "":
                    #printTS("Looking for question")
                    question = self.driver.find_element_by_class_name("quizQuestion").text
                # printTS("Found question: "+question)
                correctAnswer = self.getAnswer(quizName, question)
                #printTS("Found answer: "+correctAnswer)
                if correctAnswer == "Invalid":
                    printTS(question+" was not recognized as a question.")
                    return

                time.sleep(answerDelay)

                self.driver.execute_script("""
                    var choices = []
                    for (i = 0; i < 4; i++) {
                        choices.push(document.getElementsByClassName('answerText')[i].innerText);
                    }

                    //click on the correct answer, then hit the next quiz button
                    for (i = 0; i < 4; i++) {
                        if (arguments[0] == choices[i]) {
                            document.getElementsByName('checkboxtag')[i].click();
                            document.getElementById('nextQuestion').click();
                            break;
                        }
                    }""", correctAnswer)
                time.sleep(0.5)
            
            self.driver.find_element_by_xpath("//a[contains(@class, 'kiaccountsbuttongreen')]").click()
            printTS("Clicking")
            WebDriverWait(self.driver,15).until(lambda driver: self.driver.find_elements(By.XPATH,"//iframe"))
            iframe = self.driver.find_element_by_xpath("//iframe")
            self.driver.switch_to.frame(iframe)
            self.solveInvisibleCaptcha()
            self.driver.switch_to.default_content()
            printTS("Waiting for end text")
            WebDriverWait(self.driver,5).until(lambda driver: self.driver.find_elements(By.XPATH,"//*[contains(text(), 'Transferrable Crowns')]") or self.driver.find_elements(By.XPATH,"//*[contains(text(), 'Better luck next time!')]"))
            if len(self.driver.find_elements_by_xpath("//*[contains(text(), 'Transferrable Crowns')]")) != 0:
                self.earnedCrowns += 10
                self.activeAccountCrowns += 10
                totalCrownsEarned += 10
                printTS("Earned 10 Crowns on Account "+self.activeAccount+" with Quiz: "+quizName)
            else:
                printTS("Quiz failed, restarting...")
                self.doQuiz(quizName, quizUrl, numAttempts = numAttempts+1)
        except Exception as e:
            if numAttempts == 3:
                printTS("Following Exception occured while trying to complete the "+quizName+ " quiz. Skipping quiz.\n"+str(e))
                return
            else:
                printTS("Following Exception occured while trying to complete the "+quizName+ " quiz. Restarting quiz.\n"+str(e))
                self.doQuiz(quizName, quizUrl, numAttempts = numAttempts+1)

    def getAnswer(self, category, question):
        global switcherMagical
        global switcherAdventuring
        global switcherConjuring
        global switcherMarleybone
        global switcherMystical
        global switcherSpellbinding
        global switcherSpells
        global switcherValencia
        global switcherWizard
        global switcherZafaria

        if category == "Magical":
            return switcherMagical.get(question, "Invalid")
        if category == "Adventuring":
            return switcherAdventuring.get(question, "Invalid")
        if category == "Conjuring":
            return switcherConjuring.get(question, "Invalid")
        if category == "Marleybone":
            return switcherMarleybone.get(question, "Invalid")
        if category == "Mystical":
            return switcherMystical.get(question, "Invalid")
        if category == "Spellbinding":
            return switcherSpellbinding.get(question, "Invalid")
        if category == "Spells":
            return switcherSpells.get(question, "Invalid")
        if category == "Valencia":
            return switcherValencia.get(question, "Invalid")
        if category == "Wizard":
            return switcherWizard.get(question, "Invalid")
        if category == "Zafaria":
            return switcherZafaria.get(question, "Invalid")

    def login(self, username, password):
        global tooManyRequestsCooldown
        self.driver.get(self.login_url)
        time.sleep(1.5)
        if len(self.driver.find_elements_by_xpath("//*[contains(text(), 'Too Many Requests')]")) != 0: #Error 429 handling
            printTS("Too many requests, waiting "+str(tooManyRequestsCooldown)+" seconds for a retry. If this occurs often please increase the delay in the settings or decrease the amount of threads.")
            time.sleep(tooManyRequestsCooldown)
            self.login(username, password)
            return
        
        self.driver.execute_script("document.getElementById('loginUserName').value = '{}'".format(username))
        self.driver.execute_script("document.getElementById('loginPassword').value = '{}'".format(password))
        
        login_btns = self.driver.find_elements_by_class_name("wizardButtonInput")
        for btn in login_btns:
                if btn.is_enabled() and btn.is_displayed():
                    btn.click()
                    break
        time.sleep(3)
        #WebDriverWait(self.driver,15).until(lambda driver: self.driver.find_elements(By.XPATH,"//*[contains(text(), 'captcha')]") or self.driver.find_elements(By.XPATH,"//a[contains(@class, 'logout button orange')]"))
        iframe = self.driver.find_elements_by_xpath("//iframe")
        if len(iframe) > 0:
            self.driver.switch_to.frame(iframe[0])

        if len(self.driver.find_elements_by_xpath("//*[contains(text(), 'Please prove you are not a robot.')]")) > 0:
            self.solveVisibleCaptcha("bp_login")
        else:
            printTS("No Captcha! Login successful")
        self.driver.switch_to.default_content()

    def solveInvisibleCaptcha(self, attempts = 0):
        global captchasRequest
        global captchasFailed
        if attempts == 6:
            return False
        captchasRequest = captchasRequest + 1
        site_key = self.driver.find_element_by_class_name("g-recaptcha").get_attribute("data-sitekey")        
        #printTS("Starting Captcha Task")
        response = requests.post('https://api.capmonster.cloud/createTask', json={'clientKey': api_key, 'task': {'type':'NoCaptchaTaskProxyless', "websiteURL":"https://www.wizard101.com","websiteKey":site_key, 'userAgent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'} }).json()
        taskId = response["taskId"]
        printTS("Sent captcha to CapMonster, returned task ID: "+str(taskId))
        finished = False
        resultKey = ""
        while not finished:
            response = requests.post('https://api.capmonster.cloud/getTaskResult', json={'clientKey': api_key, 'taskId': taskId}).json()
            if response["status"] == "ready":
                finished = True
                resultKey = response['solution']["gRecaptchaResponse"]
            else:
                #printTS("Captcha not ready, response: "+json.dumps(response))
                time.sleep(5)
        
        #printTS("Finished Captcha Task, key: "+str(resultKey))
        
        self.driver.execute_script("reCaptchaCallback('{}');".format(resultKey))
        printTS("Submitting Captcha")
        time.sleep(2)
        if len(self.driver.find_elements_by_xpath("//*[contains(text(), 'There was an error')]")) > 0: #Captcha validation failed
            printTS("Captcha failed!")
            captchasFailed = captchasFailed + 1
            return self.solveInvisibleCaptcha(attempts + 1)       
        else:
            return True
    
    def solveVisibleCaptcha(self, submitBtnId, attempts = 0):
        global captchasRequest
        global captchasFailed
        if attempts == 6:
            return False
        captchasRequest = captchasRequest + 1
        site_key = "6Ld7GE0UAAAAALWZbnuhqYTBkobv6Whzl7256dQt"#self.driver.find_element_by_id("recaptcha-token").get_attribute("value")
        printTS("Starting Captcha Task")
        response = requests.post('https://api.capmonster.cloud/createTask', json={'clientKey': api_key, 'task': {'type':'NoCaptchaTaskProxyless', "websiteURL":"https://www.wizard101.com","websiteKey":site_key, 'userAgent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'} }).json()
        taskId = response["taskId"]
        printTS("Sent captcha to CapMonster, returned task ID: "+str(taskId))
        finished = False
        resultKey = ""
        while not finished:
            response = requests.post('https://api.capmonster.cloud/getTaskResult', json={'clientKey': api_key, 'taskId': taskId}).json()
            if response["status"] == "ready":
                finished = True
                resultKey = response['solution']["gRecaptchaResponse"]
            else:
                #printTS("Captcha not ready, response: "+json.dumps(response))
                time.sleep(5)
        
        #printTS("Finished Captcha Task, key: "+str(resultKey))

        #self.driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML='{}';".format(resultKey))
        self.driver.execute_script("setCaptchaInputValue('{}');".format(resultKey))
        login_btns = self.driver.find_elements_by_id(submitBtnId)
        for btn in login_btns:
            if btn.is_enabled() and btn.is_displayed():
                btn.click()
                break
        time.sleep(2)

        if len(self.driver.find_elements_by_xpath("//*[contains(text(), 'There was an error')]")) > 0: #Captcha validation failed
            return self.solveVisibleCaptcha(submitBtnId, attempts + 1)
            captchasFailed = captchasFailed + 1
        else:
            return True

def updateTotalEarned(amountToAdd):
    lock.acquire() # Aquire lock to prevent other threads opening the file while its being messed with
    path = os.path.dirname(os.path.realpath(__file__))
    with open(path+'/config.txt') as f:
        data = json.load(f)
    data["totalCrownsEarned"] = data["totalCrownsEarned"] + amountToAdd
    with open(path+'/config.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    lock.release()

if __name__ == '__main__':
    print("--------  Wizard101 Trivia Bot v"+version+" --------\n\n")
    print("--------  Gremlin Property - Test Build  --------\n\n")
    print("--------      Made with love by Tox     --------\n\n")
    print("If you encounter any issues and are on the newest version, have any suggestions or wishes for the bot feel free to contact me via Discord: ToxOver#9831")
    print("To change your settings navigate to the config.txt file and change the value to your desires")
    print("To add accounts create a new line in accounts.txt in the username:password format")
    #isVersionOutdated()

    path = os.path.dirname(os.path.realpath(__file__))
    try:
        with open(path+'/config.txt') as f:
            data = json.load(f)

        api_key = data["api_key"]
        headless = data["headless"]
        chunksAmount = data["threads"]
        tooManyRequestsCooldown = data["tooManyRequestsCooldown"]
        crownsEarned = data["totalCrownsEarned"]
        answerDelay = data["answerDelay"]
        tess.pytesseract.tesseract_cmd = data["tesseractPath"]
        printTS("Settings loaded:")
        printTS("Headless (invisible Chrome): "+("On" if headless == 1 else "Off"))
        printTS("Threads (parallel sessions): "+str(chunksAmount))
        printTS("Delay after Answer: "+str(answerDelay))
        printTS("\"Too Many Requests\" cooldown: "+str(tooManyRequestsCooldown))
        printTS("\n\nTotal Crowns earned: "+str(crownsEarned)+"\n")
    except:
        # First try loading old config, if success: make new config with old config settings + changes -> Config migration for new configs
        try:
            with open(path+'/config.txt') as f:
                data = json.load(f)

            api_key = data["api_key"]
            headless = data["headless"]
            chunksAmount = data["threads"]
            tooManyRequestsCooldown = data["tooManyRequestsCooldown"]
            crownsEarned = data["totalCrownsEarned"]
            tess.pytesseract.tesseract_cmd = data["tesseractPath"]
            data["answerDelay"] = 0.0
            answerDelay = data["answerDelay"]

            if os.path.exists(path+'/config.txt'):
                os.remove(path+'/config.txt')
            with open(path+'/config.txt', 'w') as outfile:
                json.dump(data, outfile, indent=4)

            printTS("Settings loaded:")
            printTS("Headless (invisible Chrome): "+("On" if headless == 1 else "Off"))
            printTS("Threads (parallel sessions): "+str(chunksAmount))
            printTS("Delay after Answer: "+str(answerDelay))
            printTS("\"Too Many Requests\" cooldown: "+str(tooManyRequestsCooldown))
            printTS("\n\nTotal Crowns earned: "+str(crownsEarned)+"\n")
        except:
            printTS("Failed to migrate config, creating new config...")
            if os.path.exists(path+'/config.txt'):
                os.remove(path+'/config.txt')
            with open(path+'/config.txt', 'a') as f:
                f.write("{\n")
                f.write("\"api_key\":\"PUTKEYHERE\",\n")
                f.write("\"threads\":1,\n")
                f.write("\"headless\":0,\n")
                f.write("\"tooManyRequestsCooldown\":45,\n")
                f.write("\"totalCrownsEarned\":0,\n")
                f.write("\"answerDelay\":0.0,\n")
                f.write("\"tesseractPath\":\"C:\\\Program Files\\\Tesseract-OCR\\\\tesseract.exe\"\n")
                f.write("}")
            printTS("An error occured while processing your settings. Settings have been reverted to default and can be changed in the config.txt file.\nThe bot will now close so you can change the settings to your preferences...")
            time.sleep(5)
            exit()

    if api_key is "PUTKEYHERE":
        printTS("Please set your API key from https://capmonster.cloud/ in the config.txt file.")
        time.sleep(5)
        exit()

    try:
        with open(path+"/accounts.txt") as f:
            for line in f:
                data = line.split(':')
                accountQueue.put((data[0], data[1].replace("\n", "")))
        if accountQueue.empty():
            printTS("No accounts found in accounts.txt! Please add accounts to use this bot.")
            time.sleep(5)
            exit()
    except:
        printTS("There was an error parsing your accounts.txt, make sure there are no empty lines and each line is in username:password format.")
        time.sleep(5)
        exit()
    accountsLen = accountQueue.qsize()
    response = requests.post('https://api.capmonster.cloud/getBalance', json={'clientKey': api_key}).json()
    printTS("Captcha Balance: $"+str(response["balance"]))

    try:
        threads = []
        for i in range(chunksAmount):
            bot = TriviaBot()
            t = threading.Thread(target=bot.start)
            threads.append(t)
        for x in threads:
            x.start()
        for x in threads:
            x.join()
    except:
        printTS("An outer exception occured. If this happens you've succesfully fucked something that I never thought could be fucked. Congratulations. The bot will terminate now.")
        time.sleep(10)
        exit()

    print("\n\n")
    printTS("Summary")
    printTS("Earned " + str(totalCrownsEarned)+" crowns on " + str(accountsLen) + " accounts.")
    printTS("Captcha Balance before Trivia: $"+str(response["balance"]))
    printTS("Captcha Balance after Trivia:  $"+str(requests.post('https://api.capmonster.cloud/getBalance', json={'clientKey': api_key}).json()["balance"]))
    printTS("Captchas requested: "+str(captchasRequest))
    printTS("Captchas failed: "+str(captchasFailed))

    input("Press enter to quit..")