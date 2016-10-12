# podcast_feed
We currently host our podcast on a squarespace site, and it has never validated in iTunes. This is a hack/workaround to get the feed to iTunes. Feel free to borrow/use/steal this code.

*Cronjob downloads latest squarespace XML at 20 after the hour
*Python script parses XML into SQLite db
*Flask app renders new XML feed from sqlite db that validates with iTunes
*Flask app is served via gunicorn and nginx
