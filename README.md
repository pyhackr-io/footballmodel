<!---
https://github.com/rhwilr/markdown-documentation-template/blob/master/README.md
-->
# sportbetting

## Description

The purpose of was to create an model to predict which premiership team would win a game of football based on previous years results. To make it more accurate you need consider a number of things. A few I want to add to are when I have time are.

1. Manager
2. Player Statistics
3. Fan Sentiment



## Usage

I am working on moving it from Jupyter notebooks to docker image using Python. So just Jupyter notebook within notebooks directory. It is work in progress and I will update.
```
cd <installdirectory>/SportsBookModel/notebooks
jupyter notebook
```

### Installing

Clone repo first:
```
git clone https://github.com/pyhackr-io/sportsbetting.git
```

Install the requirements file. FYI. There are a lot packages which will be installed as I have experimented with different packages to try out new features and utils.
```
pip install -r requirements.txt
```



### Folder structure

The folder structure has been created using packgenlite by [Kevin Robert](https://github.com/krokrob)

Here's a folder structure for SportBookModel :

```
SportsBookModel
├── Dockerfile
├── MANIFEST.in
├── Makefile
├── README.md
├── SportsBookModel
├── api
├── data
│   ├── datahubio
│   │   ├── data
│   ├── dataworld
│   │   ├── archive
│   │   ├── data
│   ├── football-data
│   ├── kaggleEAdata
│   ├── processed
│   └── refdata
├── notebooks
├── requirements.txt
├── scripts
├── setup.py
└── tests
```

## References

- [packgenlite](https://github.com/krokrob/packgenlite)
