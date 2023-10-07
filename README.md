# Dash for IRDC working hour

### Created by Zhidian Lin on 2022/11/5


Shift to irdc folder and Run `python ./app.py` and navigate to http://127.0.0.1:8050/ in your browser.

To update your code on web app then Run `dashtools heroku --deploy` and navigate to https://irdc-dash.herokuapp.com/. Please try not
 to open it on IE browser.
Run `dashtools heroku --update` to update the code

Please note that this is a free mode on herokuapp, only 500M Slug size for the whole project available. More details: https://dashboard.heroku.com/apps/irdc-dash/settings

Deploy new change:
$ git add .
$ git commit -am "make it better"
$ git push heroku master# irdc
# irdc

# google cloud
gcloud builds submit --tag gcr.io/irdc-all/irdc-all  --project=irdc-all

gcloud run deploy --image gcr.io/irdc-all/irdc-all --platform managed  --project=irdc-all --allow-unauthenticated


# pythonanywhere

# update new file then browse to "Web" then press "Reload irdc.pythonanywhere.com"