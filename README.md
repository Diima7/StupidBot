# StupidBot
 Record and execute mouse clicks, attached to a specific window.
 This can help you to build your own Bot easier.
### How to use it
   Right Click to start and stop recording, only left Click will be recorded.
### In Command Prompt
```
 python IdleBot.py list --> Show list of recorded files.
 python IdleBot.py [-b] [RECORD ID] --> -b to use the Bot class to execute records.
 python IdleBot.py [-r] "[WINDOW NAME]" "[RECORD FILE NAME]" --> recording mouse clicks.

 Example: python IdleBot.py -b 4
 
          python IdleBot.py -r "League of Legends" StartGame
```
## You can also use this to import it into your own programm.
### Usage:
```
   from IdleBot import Bot, record
            
   rec = record('WINDOWNAME')
   Bot = Bot('WINDOWNAME')
```
### To start record Mouse clicks you need to start listen and save it.
```
  rec.listen()
  
  # After you finished recording with right click
  # you need to save the package as a file.
  
  rec.save('NAME')
  
  # It will be saved as a ".p" file an get added to a SQL Database.
  
  rec.list() # This returns the SQL Database
```
## SQL Structure
 TABLE packages (id INT, name TEXT, time DATE, actions INT, window TEXT, WW INT, WH INT)
 Actions = len(self.data) = Number of Saved Mouse Clicks
 WW = Window width
 WH = Window height
 
### Use the Bot to execute some package.
```
   Bot.execute([ID])
```
