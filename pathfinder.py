found_path = False
diagonal = False
on_checking_event = []
on_finished_event = []

def run_algorithm(node_list, start_node, end_node):
	start_node.distance_from_start = 0
	current_node = start_node   # this list keeps track of the nodes we should check in order (lower distance from start to the higher)
	nodes_to_check = []
	while True:
		for surrounding_node in GetSurroundingNodes(node_list, current_node):
			if surrounding_node == end_node:
				return TrackBack(current_node, start_node)
			measured_distance = current_node.distance_from_start
			if surrounding_node != start_node and surrounding_node.distance_from_start > measured_distance: 
				surrounding_node.distance_from_start = measured_distance
				surrounding_node.previous_node = current_node
				if surrounding_node.is_obstacle:
					pass
				for i in range(len(nodes_to_check)):
					if nodes_to_check[i].distance_from_start > surrounding_node.distance_from_start:
						nodes_to_check.insert(i, surrounding_node)
						break
				if surrounding_node not in nodes_to_check:
					nodes_to_check.append(surrounding_node)
				CallEvent(on_checking_event, surrounding_node) # coloring the visited node
		CallEvent(on_finished_event, current_node) # coloring the current node (node that is visiting its neighbors)
		if nodes_to_check == []:
			return
		current_node = nodes_to_check.pop(0)

def TrackBack(node, start_node):
	"""
		Goes all the way back from a certain node to the start node and return the path
		*previous_node should be implemented for each node
	"""
	track_list = [node]
	last_node = node
	if node == start_node:
		return start_node
	while True:
		last_node = last_node.previous_node
		if start_node == last_node:
			return track_list[::-1] # reversing track_list
		else:
			track_list.append(last_node)

def GetSurroundingNodes(node_list, node):
	"""
		Returns all surrounding nodes without going out of node_list range
	"""
	surroundings = [(node.column, node.row-1), (node.column+1, node.row),(node.column, node.row+1)]
	if diagonal:
		surroundings += [(node.column+1, node.row+1), (node.column+1, node.row-1), (node.column-1, node.row-1), (node.column-1, node.row+1)]
	
	#Here we filter the surroundings to make sure that we don't go out of the list range
	return list(map(lambda x: node_list[x[0]][x[1]],
                        filter(lambda x: x[0] >= 0 and x[0] < len(node_list) and x[1] >= 0 and x[1] < len(node_list[0]), surroundings)))

def CallEvent(event, parameter = None):
	"""
		Call all the given event subscribers and pass the given parameter to them
			parameter: None = no parameters (Default = None)
	"""
	for function in event:
		if parameter == None:
			function()
		else:
			function(parameter)