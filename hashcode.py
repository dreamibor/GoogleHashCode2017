from collections import defaultdict,OrderedDict

class cache_server():
	def __init__(self,capacity):
		self.videos = []
		self.score = defaultdict(int)
		self.capacity = capacity
		self.influence = defaultdict(list)

	def is_empty(self):
		if self.videos == []:
			return True
		else:
			return False

class end_points():
	def __init__(self,data_center):
		self.data_center = data_center
		self.latency = defaultdict(int)
		self.requests = defaultdict(int)

'''
V (1 ≤ V ≤ 10000) - the number of videos
E (1 ≤ E ≤ 1000) - the number of endpoints
R (1 ≤ R ≤ 1000000) - the number of request descriptions
C (1 ≤ C ≤ 1000) - the number of cache servers
X (1 ≤ X ≤ 500000) - the capacity of each cache server in megabytes
'''
#file_name = "me_at_the_zoo.in"
#file_name = "kittens.in"
#file_name = "trending_today.in"
file_name = "videos_worth_spreading.in"


para_list = []
videos_list = []
endpoints_list = []
cache_server_list = []

with open(file_name) as f:
	first_line = f.readline()
	for i in first_line.split():
		para_list.append(int(i))
	
	second_line = f.readline()
	for j in second_line.split():
		videos_list.append(int(j))

	# read endpoints
	for k in range(para_list[1]):
		line = f.readline().split()
		endpoint = end_points(int(line[0]))
		for m in range(int(line[1])):
			endpoints_line = f.readline().split()
			endpoint.latency[int(endpoints_line[0])] = endpoint.data_center - int(endpoints_line[1])
		endpoints_list.append(endpoint)

	# read requests
	for n in range(para_list[2]):
		line = f.readline().split()
		endpoints_list[int(line[1])].requests[int(line[0])] += int(line[2])

for i in range(para_list[3]):
	cache_server_list.append(cache_server(para_list[4]))

for index, endpoint in enumerate(endpoints_list):
	for request, frequency in endpoint.requests.items():
		for server, latency in endpoint.latency.items():
			cache_server_list[server].score[request] += frequency * latency
			cache_server_list[server].influence[request].append(index)

for index, server in enumerate(cache_server_list):
	new_score = OrderedDict(sorted(server.score.items(), key=lambda t: t[1], reverse=True))
	for video,score in new_score.items():
	 	if server.capacity > videos_list[video]:
	 		server.capacity -= videos_list[video]
	 		server.videos.append(video)
	 		# update scores for other servers
	 		for endpoint_index in server.influence[video]:
	 			for other_server, latency in enumerate(endpoints_list[endpoint_index].latency):
	 				penalty = endpoints_list[endpoint_index].requests[video] * (endpoints_list[endpoint_index].latency[index])
	 				cache_server_list[other_server].score[video] -= penalty


# Output
total_server = 0
with open('{}.out'.format(file_name[:len(file_name)-3]),'w') as file:
	for server in cache_server_list:
		if not server.is_empty():
			total_server += 1

	file.write('{}\n'.format(total_server))

	for index, server in enumerate(cache_server_list):
		if not server.is_empty():
			output_str = "{}".format(index)
			for i in server.videos:
				output_str += " " + str(i) 
			file.write('{}\n'.format(output_str))
