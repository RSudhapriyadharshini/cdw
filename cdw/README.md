# Data Scraping

### Scrapy Projects:
- Each Category Listing Page Collection
- Each Product Detail Page Collection

### Requirements:

| Programs | Frameworks |
|----------|------------|
| Python 3 | Scrapy     |
|          | CondaEnv   |

### Conda Environment:
- In this link https://www.anaconda.com/products/individual, you can get the individual edition for installing the Anaconda.
- As I'm using ubuntu 20.04, I used this link to setup anaconda in my system.
**https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart**
- **conda create --name myenv** To create environment
- **conda activate myenv** Activate the conda environment to run scrapy in your system
- Before anaconda installation, check that your system have the latest version of python installed(Preferably python version 3)

### Requests Library:
- **pip install requests** to install requests library

### Json Module:
- **pip install json** to install json module

### Re Module:
- **pip install re** to install re module. This module supports python regex expressions

### Scrapy:
- **pip install scrapy** to install scrapy framework 

### How to run scrapy python code in your system:
- Activate the conda environment **conda activate your_env_name** in the terminal
- **scrapy crawl spider_name** to run the code
- To check the output in the form of CSV file, run the command **scrapy crawl spider_name -o file_name.csv**
**Note:** Spider name of my file is **network_adapters**

