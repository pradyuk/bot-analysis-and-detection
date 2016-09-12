# ICMP Echo Packet Flooding Detector
def detectICMPEchoFlooding(pcapRecords, thresholdPercentage, windowSize):
	instances= 0
	for index, record in enumerate(pcapRecords):
			if isICMPEchoPacket(record.protocol, record.info):		
				instances= instances + checkWindowFrame(index, pcapRecords, windowSize, thresholdPercentage)
	print '\nICMP Echo Flooding instances = ' + str(instances)
				
				
# Check how many ICMP Echo Packets are sent within the WindowSize.				
def checkWindowFrame(index, pcapRecords, windowSize, thresholdPercentage):
	windowStart = index + 1
	countInWindow = 0
	while windowStart < index + windowSize and windowStart < len(pcapRecords):
			if isICMPEchoPacket(pcapRecords[windowStart].protocol, pcapRecords[windowStart].info):
					countInWindow = countInWindow + 1
			windowStart = windowStart + 1
	if (countInWindow*100/windowSize) >= thresholdPercentage and index + windowSize < len(pcapRecords):
			print 'Detected ICMP Echo Flooding between ' + str(pcapRecords[index].timestamp) + ' and ' + str(pcapRecords[index + windowSize].timestamp) + ': ' + str(countInWindow*100/windowSize) + '%'
			return 1
	return 0
             

# Check if the current packet contributes to the ICMP Echo Flooding
def isICMPEchoPacket(protocol, info):
	return protocol=='ICMP' and all( partialDetector in info for partialDetector in ['Echo (ping)'])
