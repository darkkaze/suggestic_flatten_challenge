# Code challenge
Create a web service using any framework that flattens a nested sequence into a single
list of values.

~~~
Input:
{
"items": [1, 2, [3, 4, [5, 6], 7], 8]
}
Output:
{
"result": [1, 2, 3, 4, 5, 6, 7, 8]
}
~~~

# Endpoints

- POST /flatten  
- GET /flatten_logs  <- query the log table
- GET /docs  <-  provided by fastapi

# Docker 

~~~
docker build .

docker run -p 8000:8000 <DOCKER_ID>

~~~

#Unit Test
~~~
cd app
pytest
~~~


#Notes

write this endpoint using fastapi, sqlalchemy  and pytest 

- use sqllite for simplify the implementation (autocreate the db)
- i prefere the standar unittest module, but fastapi docs use pytest and who am i to contradict them
- I don't like the lack of clarity of how to do an isolated unit test on fastapi-pyalchemy (i prefere django for that and other reasons)


