# 🎧 MusiPy By Jenn Wang
**Description**: 


# Personality-based Music Recommendation System: 
- This music recommendation system is based on REAL psychometrically validated personality measures, not some fluffy woo-woo astrological Buzzfeed quiz stuff! 🔮🤓

- This simple project was inspired by empirical research demonstrating the links between personality dimensions and music preferences, I created this app based on _collaborative filtering_ + _content-based filtering_ using **kNN** and **cosine similarities**. Specifically, this app recommends different types of music to users based on their: 
  1) Unique personality dimensions (as validated by the psychometrically valid **Big Five Inventory**) and
  2) Real-time in-app user interactions and behaviors (e.g., 👍🏻 or 👎🏻 to a sample song snippet).
 
----------------------------------------------------------------------------------------------------------------
## **SOME UPDATES AND CAVEATS**

- This project was built a **LONG, LONG, LONG time** ago (circa ~2017) in a matter of 2-3 weeks as a beginner project for me. So, YES, I am well aware of the many errors and outdated techniques inherent in this project. Nevertheless, I wanted to share this project here in hopes of inspiring others to think about how they might try to start their very own machine learning projects even if they may not have the traditional software engineering background or training (yet) 🤓.

----------------------------------------------------------------------------------------
# **Some Common FAQs** ❓
### - *Why did you use kNN?*

  Because it is the most commonly used algorithm (the standard algorithm, if you will) for recommendation systems (as of 7 years ago when I first started this project). Also, I didn't have a lot of features in this particular dataset, so I was hoping that the potential problems of overfitting for kNN would be minimal. 

### - *Why did you use cosine similarity?*
  
  First, *cosine similarity* is a distance metric. Specifically, by measuring the **angle** between the vectors, we can get a good idea of the similarity between items. The smaller the angle, the bigger (closer to 1) the cosine value is, which is indicative of a closer similarity.

  
  I chose *cosine similarity* because it is the most commonly used distance metric, and also because the nature of my data are not "real" metric values (e.g., length, height, weight), so my thinking at the time was that distance metrics like the Euclidean metrics wouldn't be as appropriate for my particular goals. 

### - *How exactly did you use cosine similarity in your project?*

  The quick answer is that I used cosine similarity for the **personality scores** (the "content-based filtering" portion). Specifically, I used the DISTANCE between the personality scores to calculate this. I also used cosine similarity for determining song rating similarity (the "collaborative-filtering" portion, if you will).


**SUMMARY**: the inspiration behind this project was simply a way for me to see if I could creatively combine my training and background in statistics and psychology with my love of all things data and technology. While I'm sure the execution of this vision is surely primitive and crude (this was my very first web app project, after all!), I just wanted to share my work here in hopes of showing others that, even without traditional background in software engineering training, we can still create something cool and creative 💕. Learning something new is seriously so FUN! 🤓

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## **Presentation**: 

- https://github.com/wangjenn/musipy_by_jennwang/files/7940068/Public_Copy_Wang_Jennifer_MusiPy.pdf


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Quick Demo: 
- https://user-images.githubusercontent.com/12160492/151130465-aed83eab-b681-48ec-b3c3-fd01b838dc8c.mp4


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Resources: 
- Big Five Inventory (BFI): https://openpsychometrics.org/tests/IPIP-BFFM/


----------------------------------------------------------------------------------------------------------------
💕 Feel free to contact me (linkedin.com/jennifermwangphd) if you have any questions! 👍🏻. I genuinely LOVE talking to and learning from people (nerds especially welcome 🤓), but please try to remain civil and professional if possible. I welcome constructive feedback, but I don't usually find harsh criticisms or attacks on my logic and decisions very useful (yes, this has happened before, though to this day I'm not sure why). Again, I did this project a VERY, VERY LONG time ago, and I currently don't have the time nor the desire to revisit this project in depth to optimize and perfect my code to perfection. Thank you for understanding! 🙏🏻. 
