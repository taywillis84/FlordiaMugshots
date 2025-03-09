# FlordiaMugshots
Scrape Flordia Mugshot databases to develop AI model to determine where a given mugshot was taken.

##30 Row Fingerprint:
  Script that gets the top 5% of an image, calculates the expected color value of that region and saves it to a JSON file that can be used to test another photo to see how close the expected color range is to the tested image. The 30RowFingerprintTest file uses the generated fingerprint file to against a directory of photos and returns a score based on how close it is to the expected Fingerprint.

##downloadDataset:
  Collection of scripts that downloads mugshots. Scripts are avaliable for the following counties:

  Orange County, Flordia: https://netapps.ocfl.net/BestJail/Home/Inmates -- This one takes ~8 Hours to complete
  Donthan County, Alabama: https://www.dothanpd.org/news/mugshots/
  Midlands County, South Carolina: https://www.abccolumbia.com/news/mugshots/
  Montgomery County, Alabama: https://www.waka.com/mugshots/
  Jefferson County, Alabama: https://sheriff.jccal.org/NewWorld.InmateInquiry/AL0010000?Page=

##getNewMugshots_Orange:
  Script checks the counties recently bookings pdf and scrapes those mugshots only. Runs seperately because the main Orange County script takes so long. This one is a big quicker, roughly 30 minutes.

##createModel:
  Builds a model based on downloaded dataset. Organized photos in the following format - _NOTE_ images do not have to be jpg files and can be named whatever is downloaded from the website. Just organize     accordingly.:
  
dataset/
│
├── Orange_County/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── imageN.jpg
│
├── Dothan_County/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── imageN.jpg
│
├── Jefferson_County/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── imageN.jpg
│
├── Midlands_County/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── imageN.jpg
│
└── Montgomery_County/
    ├── image1.jpg
    ├── image2.jpg
    └── imageN.jpg

##testModel:
  Using the model that was created in createModel.py, categorize a new directory of images.


##Things to work on:
  Today, I do not know how to deal with mugshots that did not originate from any of these counties - not sure if that is an issue or not, but mugshots from none of these counties will return high confidence values of bing related to a county, but images originating from one of the 6 have been generally correct from my experimentation.
