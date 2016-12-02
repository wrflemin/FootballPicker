# FootballPicker

Used to make football picks based on the average weather in the home city.
This is a very accurate and well respected method for picking winning teams.

To run the project start a virtual environment and run 
```shell 
$ pip install -r requirements.txt
$ python picker.py sheets.txt secret.txt
```
where sheets.txt has the newline separated games and secret.txt has your 
secret api key for Weather Underground.
