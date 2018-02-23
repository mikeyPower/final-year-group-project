#Reducing typing load


clean_all:
	python -c "execfile('clean_db.py'); clean_all()"

clean_menu:
	python -c "execfile('clean_db.py'); clean_menu()"


clean_user:
	python -c "execfile('clean_db.py'); clean_user()"


clean_event:
	python -c "execfile('clean_db.py'); clean_event()"


clean_total:
	python -c "execfile('clean_db.py'); clean_total()"
