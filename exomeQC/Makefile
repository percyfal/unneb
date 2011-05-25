SEtest:
	if [ ! -e tmp ]; then mkdir tmp; fi
	R CMD BATCH --vanilla '--args exomerc="exomeSE.yaml"' exomeQC.R exomeQC-SE.Rout

PEtest:
	if [ ! -e tmp ]; then mkdir tmp; fi
	R CMD BATCH --vanilla '--args exomerc="exomePE.yaml"' exomeQC.R exomeQC-PE.Rout

test: PEtest SEtest

clean:
	rm -rf tmp
