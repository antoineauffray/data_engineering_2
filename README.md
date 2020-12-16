# Web Application

### Running docker application

#### • Download the repository

	mkdir file
	cd file
	git clone https://github.com/MANT3QUILLA/data_engineering_2.git
	cd data_engineering_2
	
#### • Run the docker image

	docker-compose up
	
### • Running tests

##### 1. Unit test

	python unittest_model.py
	
##### 2. Integration test

	python integration_test.py
	
##### 3. Stress test
	
	python model.py
	ab -n 1000  http://0.0.0.0:5000/
	
	
	
