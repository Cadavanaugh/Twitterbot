# TwitterBot GUI

I made this program to make easier the creation of Twitter Bots. The graphical interface eases the process, with no need to write code.
The program was written in **Python3** using Twitter's API v1.1 to gather the data and execute the actions.


## Dependencies
In order to the script run correctly you'll have to install two third-party modules:
- Tweepy
- PIL

Just use the commands shown below in your terminal.
```
pip install tweepy Pillow
```

## How does it work

When running the script for the first time a "Bot Settings" window will appear for you to input the necessary data.

![Settings](/img/settings.png)

In the **Keys & Tokens** section you have to input the four required API Keys.

In the **Search for tweets** field you'll input the word you want the bot to interact with.

Hitting the **ENTER** button will create a "_settings.txt_" file which will storage all the previous data. "Bot Settings" will close automatically.

![BotGUI](/img/gui.png)

Now just input the @ and click START BOT. The border will turn green and a terminal will show up.

![BotGUI working](/img/working.png)

In case of errors a warning window will pop-up with more details. Feel free to modify the code.