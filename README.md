# 4300 Final Project: Nutrition Dashboard

## Project File Structure

| File | Purpose |
|------|---------|
|`app.py`|Front page of Streamlit app (navigation & landing page)|
|`pages/upload.py`|Upload CSV page → Uploads to S3 raw bucket|
|`pages/analytics.py`|Analytics page → Pulls cleaned data from S3 processed bucket & visualizes nutrition data|
|`utils/s3_uploader.py`|Handles connecting to S3 & uploading user-uploaded CSVs to raw bucket|
|`utils/s3_downloader.py`|Handles connecting to S3 & downloading cleaned data from processed bucket|
|`config.py`|Stores secrets & manages AWS connection variables for local use (loaded from `.env`)|


## Setup directions
1. if needed copy code to ubuntu run
```
scp -i path/to/your/key-pair.pem clean_upload.zip ubuntu@ec2-instance-public-ip-address
# clean upload.zip should only include app.py, pages, s3 upload/downlaod utils, requirements.txt, and deploy (with ec2_setup.sh)

```

2.  ssh in to AWS 
```
ssh -i path/to/your/key-pair.pem ubuntu@ec2-instance-public-ip-address
```
3. download requirements and set up ec2 instance in ubuntu. This only needs to be run once, or if your ubuntu venv was deleted somehow. 

```
bash ec2_setup.sh # creates venv for running ec2 instance with streamlit app code
```
4. unzip zipped code 

```
unzip -o your-zip-file.zip
```
5. run: 

```
streamlit run app.py
```