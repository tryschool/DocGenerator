install:
	bash install.sh

run:
	python3 main.py templates/test_template.odt test_template.pdf '{"firstname": "Robert", "lastname": "Houdin", "age": 21, "period_array": [{"start_period": "10-09-24", "end_period": "10-10-24", "period_project": "RedSteel"}, {"start_period": "10-11-24", "end_period": "10-12-24", "period_project": "my_tar"}]}'
