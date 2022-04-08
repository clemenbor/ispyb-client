from operator import itemgetter

def printConfiguration(proposal, password, url):

	print("\n\n-------------------")
	print("Configuration Values")
	print("-------------------")
	print("proposal/user:   %s" % str(proposal))
	print("password:   %s" % str(password))

def printify(value):
	return str(value).ljust(22, ' ')

def getMeasurements(experiment):
	measurements = []
	for sample in experiment.samples:		
		measurements = measurements + sample.measurements
	return sorted(measurements, key=itemgetter('priority')) 

def printMeasurement(measurement):
	print("\t%s|%s|%s|%s|%s" % (printify(measurement.comment), printify(measurement.specimenId), printify(measurement.measurementId),printify(measurement.viscosity), printify(measurement.code)))
		
def printExperiment(experiment):
	print("\n\n-------------------")
	print("Experiment")
	print("-------------------")
	print("Name     %s" % str(experiment.name))
	print("ID       %s" % str(experiment.experimentId))
	print("Date     %s" % str(experiment.creationDate))	

	print("\t\n[Specimens]")
	
	print("\t%s|%s|%s|%s|%s" % (printify("Macromolecule"), printify("bufferId"), printify("Concentration"), printify("Volume"), printify("SpecimenId")))
	for sample in experiment.samples:
		if (hasattr(sample, 'macromolecule3VO')):
			print("\t%s|%s|%s|%s|%s" % (printify(sample.macromolecule3VO.acronym), printify(sample.bufferId), printify(sample.concentration),printify(sample.volume), printify(sample.specimenId)))
		else:
			print("\t%s|%s|%s|%s|%s" % (printify(""), printify(sample.bufferId), printify(sample.concentration), printify(sample.volume), printify(sample.specimenId)))

	


	# Sorting measurements by priority 
	measurements = getMeasurements(experiment)

	print("\t\n[Measurements]")
	print("\t%s|%s|%s|%s|%s" % (printify("Comment"), printify("Temperature"), printify("Priority"), printify("Volume"), printify("Specimen")))
	print("\t%s" % ("-".ljust(22*5, '-')))

	for measurement in measurements:
		print("\t%s|%s|%s|%s|%s" % (printify(measurement.comment), printify(measurement.exposureTemperature), printify(measurement.priority), printify(measurement.volumeToLoad), printify(measurement.specimenId) ))
