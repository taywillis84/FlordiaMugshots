# FloridaMugshots

This project scrapes Florida mugshot databases to develop an AI model that can determine where a given mugshot was taken.

---

## 30 Row Fingerprint

The `30RowFingerprint` script extracts the top 5% of an image, calculates the expected color values of that region, and saves the data to a JSON file. This fingerprint file can then be used to test another image by comparing the color range of the tested image against the expected fingerprint. The `30RowFingerprintTest` file uses the generated fingerprint file and evaluates a directory of photos, returning a score based on how closely the tested image matches the expected fingerprint.

---

## downloadDataset

This collection of scripts downloads mugshots from various counties. The following counties are supported:

- **Orange County, Florida**: [https://netapps.ocfl.net/BestJail/Home/Inmates](https://netapps.ocfl.net/BestJail/Home/Inmates)  
  _(This download process takes approximately 8 hours.)_

- **Dothan County, Alabama**: [https://www.dothanpd.org/news/mugshots/](https://www.dothanpd.org/news/mugshots/)

- **Midlands County, South Carolina**: [https://www.abccolumbia.com/news/mugshots/](https://www.abccolumbia.com/news/mugshots/)

- **Montgomery County, Alabama**: [https://www.waka.com/mugshots/](https://www.waka.com/mugshots/)

- **Jefferson County, Alabama**: [https://sheriff.jccal.org/NewWorld.InmateInquiry/AL0010000?Page=](https://sheriff.jccal.org/NewWorld.InmateInquiry/AL0010000?Page=)

---

## getNewMugshots_Orange

This script checks for the most recent bookings in Orange County, Florida, and only scrapes those mugshots. It runs separately from the main Orange County script because the main process takes a long time. This script is much faster, completing in roughly **30 minutes**.

---

## createModel

This script builds a machine learning model based on the downloaded dataset. The images should be organized in the following folder structure:  

**_Note:_**  
The images do not have to be in `.jpg` format and can be named however the website provides. Just make sure to organize them accordingly.

```
dataset/
│ ├── Orange_County/ 
    ├── image1.jpg │
    ├── image2.jpg │
    └── imageN.jpg │
  ├── Dothan_County/ 
    ├── image1.jpg │
    ├── image2.jpg │
    └── imageN.jpg │
  ├── Jefferson_County/ 
    ├── image1.jpg │
    ├── image2.jpg │
    └── imageN.jpg │
  ├── Midlands_County/ 
    ├── image1.jpg │
    ├── image2.jpg │
    └── imageN.jpg │
  └── Montgomery_County/
    ├── image1.jpg
    ├── image2.jpg
    └── imageN.jpg
```

---

## testModel

Using the model that was created in the `createModel.py` script, this function categorizes a new directory of images based on the learned dataset.

---

## Things to Work On

Currently, there is no handling for mugshots that do not originate from any of the supported counties. While it hasn't been a significant issue in my experiments, mugshots from counties outside the six listed may return high confidence values as being related to a county, even if they are not correct. Further improvements in handling non-county images are needed.

---

Feel free to contribute and improve upon this project!
