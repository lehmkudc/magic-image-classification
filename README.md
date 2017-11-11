# magic-image-classification

## At a glance Status:
The basic script of generating data is writen and appears to work fine. I still need to get a device to run it for ~7 hours to get my training data setup and deposited into SQL. If possible I would like to make my image generating function more efficient, as it is easily the largest bottleneck in the code clocking in at ~2 seconds per card image I'm trying to dirty. Granted its much faster than the proof of concept project from a year ago since im not messing with os commands too much.

### Q: What is this project about?
A: My goal is to generate procedurally generated noise for Magic the Gathering cards as a training set for a machine learning model that classfifies them.

### Q: What is Magic the Gathering?
A: Magic the Gathering is a trading card game developed by Wizards of the Coast and owned by Hasbro. It's the most popular TCG in the country and has competitive tournaments all across the world. The recent 2017 World Championship boasted a first prize of $100,000. I play this game fairly competitively as well, and spend a fair amount of my time playing, theorycrafting, or otherwise interacting with Magic. As it is a successful TCG, many of its cards have significant value and even have their own seconday market, with single prices of cards reaching tens of thousands of dollars. Most repeat players have some sort of trading binder with cards displayed for trading, but the actual price of these cards varies depending on the market. Typing in the card name on a phone is fraugt with autocorrect flubs and is generally a painful process. Being able to take a picture of a card or binder page and translating that information into card names and editions, linking that data to a price aggregator, and totaling that informaiton would be invaluable to a practicing magic player.

![Here's a Magic Card](https://img.scryfall.com/cards/small/en/m10/146.jpg?1510053183)

### Q: Why address this project at all? Doesn't TCGPlayer already have a fairly sucessful app that does pretty much this?
A: Yes, but this project is not for selling. I'm doing this project for a number of reasons:  
-- I'm building a portfolio for employment.   
-- My old roommate and I started work on this project before their app was announced.  
-- I have a lot of dumb project ideas and this one seemed the most approachable.  
-- A wonderful excuse to learn some data management concepts and actually use SQL outside of a youtube tutorial.  
-- I have a soft spot for numerical simulations. I probably wouldn't start this project if the messy data generation aspect wasn't a core component.  
-- If I do eventually make an android app of this or something, there are a number of additions I would like to make compared to the TCG app.   

### Q: Why are you generating your image data?
A: This is sort of the point of this project. Obtaining hundreds or thousands of pictures of each card isnt particularly reasonable with the resources I have available. However this could also extend to other image modeling problems where obtaining a significant amount of data from the process you are hoping to model is simply not possible. There has been some precident for biology applications where a research group [I'll post the link when I find it again] used image processing to make an image appear as though it were percieved thorugh a microsope. While that was a much more targeted application of data generation through image processing, this project is intended to be an experiment to see how well my simulated dataset can model camera photos. I do recognize the large issue of creating a model using a fundamentally different data generaiton process as the training set. The end goal for this project is general ability to classify images, it really doesnt have to be perfect.

### Q: Why are you storing your images as hashes instead of numpy arrays? We have image pocessing packages and have a large library of computer vision modeling to work with.
A: I'm broke and just dont have the storage space for that. Not only that, but since this project is an excuse to get comfortable interfacing python and SQL, I really dont want to have to design a 700 by 500 pixel database with the knowledgebase that I have. My budget is literally 0, and my personal devices have 4gb of storage left between the two. Let's just call this process another experiment. As this project develops and more resources are available, this is probably the first structural change I'll be addressing.

### Q: Where are you getting your initial image data?
A: Scryfall API: https://scryfall.com/docs/api

### Q: Gah this is a mess! How do you even run this thing?
A: Sorry I'm pretty new to this software development thing, as I'm just used to making jury-rigged scripts as final products. Right now running the data_generation.py script is how you run everything I have setup and working.

### Q: You mentioned a proof of concept? Where/What is this?
A: As a capstone project for my deep learning class, my old roommate and I worked together to classify images from the Kaladesh expansion. As far as POC's go this was quite effective despite all the glaring mistakes and lazy programming we did. We managed to get 99.9% accuracy of our test dataset (which was still simulated so its not really that impressive), though we plugged in like 3 images taken via iphone and they were classified correctly as part of our presentation so we were pretty happy with that. Also it's done entirey by jupyter notebook so its not quite "run" able. I'll probably clean it up eventually so everyone can point and laugh at how bad my python programming and organization was.  
GitHub Link: https://github.com/lehmkudc/Card-Image-Classifications-with-NN
Submitted Report: https://docs.google.com/document/d/1Tgr4ey50NkHicyu2NtYWG_PBR5sh2KAL23ARAN48a_4/edit?usp=sharing


Thank you for taking the time to look over my work on this independent project of mine. If you want to ask me questions about it or about me, please email me at LEHMKUDC@gmail.com.
