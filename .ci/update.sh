# Stop the current version of the site
docker rm -f capstone_site

# Pull new version
cd ~/capstone_site && git pull;