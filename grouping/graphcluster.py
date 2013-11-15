import random

def score(profile1, profile2, cache):
    """ Calculate the score from profile1 to profile2 """
    # Note: score(x,y) != score(y,x) from the API
    # so we calculate rscore(x,y) = score(x,y) + score(y,x) 
    # so that rscore(x,y) == rscore(y,x)

    score = 0
    hits = 0
    if profile1 in cache:
        if profile2 in cache[profile1]['suggest']:
            ++hits
            score = cache[profile1]['suggest'][profile2]

    if profile2 in cache:
        if profile1 in cache[profile2]['suggest']:
            ++hits
            score += cache[profile2]['suggest'][profile1]

    if hits == 2:
        score /= 2

    return score


class GraphCluster(object):
    """ This algorithm clusters a graph into a number of fixed sized groups
        The last group may contain less elemnts.
    """
    def __init__(self, group_size, adjacency_list):
        self.adjlist = adjacency_list
        self.group_size = group_size

        elements = adjacency_list.keys()
        # shuffle elements  
        elements = random.sample(elements, len(elements))
        self.groups = [ {element: 0 for element in elements[i:i+group_size]} for i in range(0, len(elements), group_size) ]
        self.update_group_scores()


    def update_group_scores(self):
        """ update the stored score for every element in its current group """
        for gn, group in enumerate(self.groups):
            for element in group:
                group[element] = self.group_score(element, [p for p in group if p != element])


    def group_score(self, element, group_elements):
        """ calculate the total score for a element in a group """
        f = lambda x: score(x, element, self.adjlist)
        return sum(map(f, group_elements))


    def step(self):
        """ step the algorith once """
        for gn, group in enumerate(self.groups):
            for element in group:
                # calculate a group score for element in all other groups
                group_scores = [self.group_score(element, g) for g in self.groups]
                # check if another group has a higher score
                best_score = max(group_scores)
                bgi = group_scores.index(best_score)
                if bgi != gn:
                    # find weakest element in other group
                    worst_element, worst_score = reduce(lambda x,y: x if x[1] < y[1] else y, self.groups[bgi].items())
                    # calculate score for worse_element in current group
                    new_score = self.group_score(worst_element, [g for g in group if g != element])
                    # check if the swap will make the total score better
                    if new_score + best_score > group[element] + self.groups[bgi][worst_element]:
                        # do swap
                        del group[element]
                        group[worst_element] = new_score
                        del self.groups[bgi][worst_element]
                        self.groups[bgi][element] = best_score
                        #NOTE: not the true score since we removed the worst element!
        # update group scores
        self.update_group_scores()
