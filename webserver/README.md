# Web Server
This Web server allows you to interact with the senvironment monitor and will allow you to:

-[ ] Log in to see any data
-[ ] Provide a home page with most current image from the camera and past day's historical (Temp, Humidity, Pressure (THP))
-[ ] Allow you to go back in time and look at historical values
-[ ] Allow you to add timestamped notes
-[ ] Let you fire off timed actions

It's a flask app. Most pages will be done in Vue. The pages will not be pre-compiled until we get this project well off the ground, but they will be tiny so it should be OK (right?). The code is derived from 
Anthony Hubert's excellent (Digital Ocean Tutorial)[https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login]. This got tis started very quickly, and many thanks to him. 

## Environment Variables

* DATABASE_URL - Defaults to sqllite:///var/pi-env/db.sqlite. We onlt install drivers for SQLite, so if you want to use something else, make sure you install the python drivers
* SECRET_KEY - Used to sign the JWTs. If not supplied, we re-create them on startup and the value is written to the logs. 

# TODO

-[ ] User Auth API
-[ ] Basic Front end to show the current pictures and graph
-[ ] REST API
-[ ] Front end that lets you move historically
-[ ] Allow adding comments, naming the grow, and having a day counter
-[ ] An interface for you to run a script at set intervals
-[ ] An interface to let you use the output in PWM mode on a timer (light timer)
-[ ] An interface to let you use the outputs in response to inputs
