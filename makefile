
run:
	export FLASK_APP=LeFacubier; export FLASK_DEBUG=1; python run.py;

run_no_debug:
	export FLASK_APP=LeFacubier; export FLASK_DEBUG=0; python run.py;

#exit the dev environment
exit:
	deactivate

#enter the dev environment
enter:
	source env/bin/activate
