import time
on_checking_event = []
on_finished_event = []

def FindPath(node_list, start_node, end_node):
	"""
		Encontra um caminho entre dois nodos (start_node) e (end_node) num mapa de nodos (node_list)
	"""
	start_node.distance_from_start =  0
	current_node = start_node
	to_check = []
	while True:
		for surrounding_node in GetSurroundingNodes(node_list, current_node):
			if surrounding_node == end_node:
				return TrackBack(current_node, start_node)
			if surrounding_node.distance_from_end == float("inf"):
				surrounding_node.distance_from_end = GetNodeDistance(surrounding_node, end_node)
				surrounding_node.previous_node = current_node
				CallEvent(on_checking_event, surrounding_node)
				for i in range(len(to_check)):
					if to_check[i].distance_from_end > surrounding_node.distance_from_end:
						to_check.insert(i, surrounding_node)
						break
				if surrounding_node not in to_check:
					to_check.append(surrounding_node)
		CallEvent(on_finished_event, current_node)
		if to_check == []:
			return
		current_node = to_check.pop(0)

def GetSurroundingNodes(node_list, node):
	"""
		Retorna todos os nodos ao redor do nodo passado como argumento (node)
		Estes nodos sao os utilizados para explorar o caminho ate o destino.
	"""
	surroundings = [(node.column, node.row-1), (node.column, node.row), (node.column, node.row+1), (node.column-1, node.row)]

	# Filtra alguns nodos que saem fora do mapa
	return list(map(lambda x: node_list[x[0]][x[1]],
                        filter(lambda x: x[0] >= 0 and x[0] < len(node_list) and x[1] >= 0 and x[1] < len(node_list[0]), surroundings)))

def GetNodeDistance(node, target):
	"""
		Retorna a distancia de um nodo (node) ate o alvo (target)
	"""
	return abs(node.column - target.column) - abs(node.row - target.row)

def TrackBack(node, start_node):
	"""
		Retorna o caminho entre dois nodos apos a pesquisa atingir o nodo alvo (node) partindo do nodo (start_node)
	"""
	track_list = [node]
	last_node = node
	if node == start_node:
		return start_node
	while True:
		last_node = last_node.previous_node
		if start_node == last_node:
			return track_list[::-1]
		else:
			track_list.append(last_node)

def CallEvent(event, parameters):
	"""
		Chama eventos. Usado para colorir alguns nodos a medida que sao explorados.
	"""
	for function in event:
		function(parameters)
