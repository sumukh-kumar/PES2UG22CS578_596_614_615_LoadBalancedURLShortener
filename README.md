# PES2UG22CS578_596_614_615_LoadBalancedURLShortener


## Week 1
### To run 
#### First run redis container - docker run -d --name redis -p 6379:6379 redis
#### Then build the dockerfile - docker build -t url-shortener ./app
#### Run the dockerfile        - docker run -d --name url-app --link redis -p 5050:5000 url-shortener
#### The website should be hosted on localhost:5050 ![URL Shortener Interface](./mdimages/output_week1.png)