# Pull new version
cd ~/capstone_site && git pull;

# build and deploy
cd .ci && docker-compose build --no-cache --build-arg loki_user=${loki_user} --build-arg loki_pass=${loki_pass};
cd .ci && docker-compose up -d;

# Notify that new version is up
curl -X POST -d "Body=New version of capstone.sethangell.com has been deployed" -d "From=$twilio_number" -d "To=$to_number" "https://api.twilio.com/2010-04-01/Accounts/$twilio_sid/Messages" -u "$twilio_sid:$twilio_token"

