# Set working directory
# First attemps to cd into .ci, if that fails try from one level up
cd .ci || cd capstone_site/.ci

# build and deploy
docker-compose build --no-cache --build-arg loki_user=${loki_user} --build-arg loki_pass=${loki_pass};
docker-compose up -d;

if curl 'https://capstone.sethangell.com'
# Notify that new version is up
then curl -X POST -d "Body=New version of capstone.sethangell.com has been deployed" -d "From=$twilio_number" -d "To=$to_number" "https://api.twilio.com/2010-04-01/Accounts/$twilio_sid/Messages" -u "$twilio_sid:$twilio_token"
# notify that the curl was not a success
else curl -X POST -d "Body=The deployment of capstone.sethangell.com seems to have hit a snag" -d "From=$twilio_number" -d "To=$to_number" "https://api.twilio.com/2010-04-01/Accounts/$twilio_sid/Messages" -u "$twilio_sid:$twilio_token"
fi