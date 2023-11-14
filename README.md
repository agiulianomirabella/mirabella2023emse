# mirabella2023emse
Machine Learning-driven Testing of Web APIs

Steps to reproduce the experiments:
- `pip install -r requirements.txt`
- `cd MALTA`
- `python manage.py runserver`
- Open RESTest with IntelliJ or similar
- choose a service to test (e.g. GitHub)
- In the service's properties path (e.g. src/test/resources/GitHub/props.properties), modify the property "generator" accordingly to your desired method (choose "RT" for SOTA or "MLT" for MALTA)
- In the service's properties path (e.g. src/test/resources/GitHub/props.properties), modify the property "experiment.name" so not to overwrite previous experiments
- In src/main/java/es/us/isa/restest/main/TestGenerationAndExecution.java, write the path to the service's properties path (e.g. "src/test/resources/GitHub/props.properties")
- Execute src/main/java/es/us/isa/restest/main/TestGenerationAndExecution.java

Stepts to reproduce the analysis of experiments results:
- `pip install -r requirements.txt`
- `cd exp1` (exp2, exp3, or performance)
- `python main.py`