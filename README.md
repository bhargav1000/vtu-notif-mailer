# VTU Notification Mailer

BeautifulSoup based notification scraper for the VTU website written in Python. This script scrapes notifications from Visvesvaraya Technological University(VTU) [website](http://vtu.ac.in/) and sends the most relevant notifications based on keyword searches in each notifications. Documents such as PDFs within the notification links are also scraped and sent as a compressed file to the recipients specified in the mailing list. This has helped several faculty members receive notifications and stay up to date on the latest events in VTU. A custom cron job can be added to the script to deliver timely updates.

## Requirements:
- BeautifulSoup 4.8.1


## Getting Started:
- Add your email credentials in the areas specified.
(You need to provide access to less secure apps in Google Security Settings or your email settings otherwise you will be unable to send emails to the recipients. Also make sure not to spam your recipients mailbox, everyone wants a clean inbox after all.)

- To run the script type ```python3 vtunotifmailer.py``` on the command line and check your inbox.

Currently works in Linux and OS X only, will release a Windows version soon :P


