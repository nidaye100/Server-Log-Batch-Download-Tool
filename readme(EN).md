# How to Download Logs for Players Using Exaroton Vanilla Server Core?

If you're a player using the Exaroton vanilla server core and want to access previous server logs without frequently downloading them manually,  
this project will help you!

When using the vanilla core—i.e., the core without plugins—the server logs only retain the content from the last server session.  
In other words, when you restart the server, the new logs will overwrite the previous ones.  
By using this project, you can easily fetch and download each log in the background, saving it to your specified location.  

# How to Use?
In the "Code" section, you will find a folder named * *Log Auto-Download Tool* *. Download it.  
Inside the folder, there are two files: an executable program and a configuration file.  
Before opening the executable file (the .exe file), you need to first open the configuration file config.json  
and enter your API key and server ID in the corresponding fields, then save the file.  

## How to Get Your API Key and Server ID?
Getting your API key is simple. Just go to your account page, scroll down to find the hidden API token,  
that long string of characters is your API key.  

Getting your server ID is a bit more complicated.  
First, press the Win key and R at the same time to open the "Run" dialog, then type cmd  
and press Enter. This will open the command prompt. Now, type the following command:  

```
curl -X GET "https://api.exaroton.com/v1/servers" -H "Authorization: Bearer YOUR_API_KEY"
```
(Replace the YOUR_API_KEY part with your own API token)  
Press Enter, and you will receive a lot of information about your server.   
The first id from left to right is your server ID.  

Now you have your server ID and API token.  
Enter them in the corresponding parts of the configuration file, save it, and exit.  
(Note: the configuration file needs to be in the same directory as the executable file, i.e., in the same folder)  

# How to View the Program’s Running Process?
Once everything is set up, double-click the executable file, and the command prompt and the program will open together.  
The program will first ask you to choose the log save location. This prompt will appear only the first time you open the program;   
it will not ask again during subsequent runs.  
The feedback from the program will be displayed in the command prompt that is opened alongside it.

### How to Package
This program is written in Python and packaged into an executable using [PyInstaller](https://pyinstaller.org/en/stable/).

To package the program yourself:
```bash
pyinstaller --onefile main.py

