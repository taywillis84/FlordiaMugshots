# FloridaMugshots

This project scrapes Florida mugshot databases to develop an AI model that can determine where a given mugshot was taken.

---

## downloadDataset

This collection of scripts downloads mugshots from various counties. The following counties are supported:

- **Orange County, Florida**: [https://netapps.ocfl.net/BestJail/Home/Inmates](https://netapps.ocfl.net/BestJail/Home/Inmates)  
  _(This download process takes approximately 8 hours.)_

- **Midlands County, South Carolina**: [https://www.abccolumbia.com/news/mugshots/](https://www.abccolumbia.com/news/mugshots/)

- **Jefferson County, Alabama**: [https://sheriff.jccal.org/NewWorld.InmateInquiry/AL0010000?Page=](https://sheriff.jccal.org/NewWorld.InmateInquiry/AL0010000?Page=)

---

## downloadRecent_OrangeCounty

This script downloads the recent arrest report from the past 24 hours, scrapes the PDF and only downloads those new mugshots from Orange County. This is significantly faster than downloading the database as done previously.

---

## createTestDataset

Randomly selects 20% of the downloaded dataset from each county and moves it to a new directory called ``` testImage ```. This will be the test dataset used by the AI training model.

---
## buildModel

This script builds a machine learning model based on the downloaded dataset. The images should be organized in the following folder structure:  

**_Note:_**  
The images do not have to be in `.jpg` format and can be named however the website provides. Just make sure to organize them accordingly.

```
trainingData/
  ├── Jefferson/ 
    ├── image1.jpg │
    ├── image2.jpg │
    └── imageN.jpg │
  ├── MIDLANDS/ 
    ├── image1.jpg │
    ├── image2.jpg │
    └── imageN.jpg │
  ├── Orange/ 
    ├── image1.jpg │
    ├── image2.jpg │
    └── imageN.jpg │

```

---

## testModel

Using the model that was created in the `buildModel.py` script, this function categorizes a new directory of images based on the learned dataset and displays it with a Saliency map for each image. I persoanlly recommend moving photos that the AI has not been trained on and testing them during this phase, specifically new mugshots that have been taken after the model has been deployed.

---

## Things to Work On

Currently, there is no handling for mugshots that do not originate from any of the supported counties. While it hasn't been a significant issue in my experiments, mugshots from counties outside the six listed may return high confidence values as being related to a county, even if they are not correct. Further improvements in handling non-county images are needed.

---

## Potential Issues

I have no idea if the resultion of the image plays a part here - the script will convert all images to a standard size before training the model, but I have yet to determine if that has a strong impact on model training. Does the model know a mugshot is Orange County simply because of the resolution artifacts or is it picking up on other things?
