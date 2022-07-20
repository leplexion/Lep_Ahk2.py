set http_proxy=http://localhost:1080
set https_proxy=http://localhost:1080
git config --global http.sslVerify "false"
git add .
git commit -m "update"
git push