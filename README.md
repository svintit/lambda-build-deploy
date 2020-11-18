# lambda-build-deploy

Repository for all serverless functions

## To build
```shell script
./scripts/build
```
This has 6 steps: 
1. Building of private dependancies
2. Building of code and public depenancies
3. Injection of private dependancies into build
4. Cleaning of build
5. Compression of build
6. Extraction of compressed build

No args.

## To deploy
```shell script
./scripts/deploy --region eu-west-1 --environment dev
```
This has 2 steps: 
1. Uploading code to appropriate s3 bucket with the appropriate filename
2. Update function code from s3 bucket.

2 args:
- `-r | --region`: aws region to deploy to, requires full region name. - [us-east-1, eu-west-2]
- `-e | --environment`: environment to deploy to, set possible values. - [dev, ci, test, prod]

Arguments default to:
- `-r | --region` = ci
- `-e | --environment` = eu-west-1


### Run commands together:
```shell script
./scripts/build && ./scripts/deploy --region eu-west-1 --environment dev
```
