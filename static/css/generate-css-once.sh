# Make sure that compass is installed!
# gem install compass

compass compile -I sass .
cp stylesheets/* .
rm -Rf stylesheets
