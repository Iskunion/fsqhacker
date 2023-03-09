APKLIST = $(foreach n,$(shell echo *.apk),$(basename $(n)))
# NEWAPKLIST = $(addprefix output/,$(shell echo *.apk))
SIGNPWD = 123456
## change it to your own
PYTHON = "/c/Program Files/Python310/python"

ALL: depackage package modify repackage sign run
	@echo All things are done!

$(shell mkdir -p output)
$(shell mkdir -p result)

depackage:
	@echo Detected `echo $(APKLIST) | wc -w` apk\(s\).
	@for i in $(APKLIST); do echo depackaging $$i.apk... && apktool d -s $$i.apk;done
 
modify:
	@echo processing pngs in res...
	@for i in $(APKLIST);do find $$i/res/ | grep --regex ".*\.png" | xargs $(PYTHON) dissimulator.py;done
	@echo processing xmls in res...
	@for i in $(APKLIST);do find $$i/res/ | grep --regex ".*\.xml" | xargs $(PYTHON) dissimuxml.py;done
	@echo processing pngs in assets...
	@for i in $(APKLIST);do find $$i/assets/ | grep --regex ".*\.png" | xargs $(PYTHON) dissimulator.py;done
	@echo processing xmls in assets...
	@for i in $(APKLIST);do find $$i/assets/ | grep --regex ".*\.xml" | xargs $(PYTHON) dissimuxml.py;done

package:
	@echo Leave apks in $(abspath output)
	@for i in $(APKLIST);do echo packaging $$i.apk && apktool b $$i -o output/$$i.apk;done

test:
	@echo $(APKLIST)
	@echo $(NEWAPKLIST)

repackage:
	@echo Leave modified apks in $(abspath output)
	@for i in $(APKLIST);do echo packaging $$i.apk && apktool b $$i -o output/$$i-modified.apk;done

sign:
	@echo signing...
	@for i in $(APKLIST);do echo $(SIGNPWD) | jarsigner -keystore apks -signedjar output/$$i.apk output/$$i.apk apks;done
	@for i in $(APKLIST);do echo $(SIGNPWD) | jarsigner -keystore apks2 -signedjar output/$$i-modified.apk output/$$i-modified.apk apks2;done

run:
	@echo runing
	@for i in $(APKLIST);do java -jar fsquadra/FSquaDRA.jar output/$$i.apk output/$$i-modified.apk -o result/result-$$i.csv;done
	@find . | grep result- | xargs $(PYTHON) csvmerger.py

clean:
	-@for i in $(APKLIST);do rm -r $$i;done

clean-all: clean
	-@if [ -e output ]; then rm -r output; fi;
	-@if [ -e result ]; then rm -r result; fi;
	-rm *.csv