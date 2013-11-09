'''
Created on 09/nov/2013

@author: mlarocca
'''
from random import randrange, randint
import logging

def generate_n_points(n):
  """ Randomly generate n random points in a one-dimensional space.
      :param n: The number of points to generate
      :type n: int
      :return: A list of n+1 values: The first value will always be 0 (the origin), 
                while the next n ones will be the coordinates of the points in a one-dimensional 
                coordinate system. All values are positive.
                [To obtain a random set of positive and negative points, choose a random value
                 from the set returned and subtract it from all the others:
                 from random import choice
                 p = choice(points)
                 map(lambda x: x-p, points)
                ]
  """
  if n < 1:
    logging.warn("[generate_n_points] Illegal parameters n: %s" % str(n))
    return 
  
  exp = randint(2, 10)
  max_dist = randint(n, n ** exp)
  start = 0
  points = [0]  #first point, can always be thought on the origin, without loss of generality
  for _ in xrange(n):  
    start += randint(1, max_dist)
    points.append(start)
    
  return points
  
############################
#  TURNPIKE PROBLEM
############################

def turnpike_random_instance(n_points):
  """ Generate a random instance of the Turnpike problem.
      :param n_points: The number of points to be placed on the circle
      :type n_points: int
      :invariant: n_points > 1 At least two points are needed for a meaningful instance
      :return: A sorted list of n_points * (n_points-1) + 2 distances, including 0 and 
                 the circumference of the circle on which the points lies
  """
  if n_points < 2:
    logging.warn("[beltway_random_instance] Illegal parameters n_points: %s" % str(n_points))
    return
  #else
  points = generate_n_points(n_points + 1)  #The extra point will represent the length of the segment after the last point
  segment_length = points.pop(n_points + 1)
  
  return turnpike_compute_distances(points, segment_length)

def turnpike_compute_distances(points, segment_length):
  """ Given a set of points, create an input for the Turnpike problem;

      :param points: The list of points from which the instance have to be created.
      :type points: list
      :invariant: The elements of points must be sorted in ascending order.
      :param segment_length: The total length of the segment.
      :type segment_length: int      
      :return: A sorted list of n * (n-1) + 2 distances (where n == len(points)),
               including 0 and the circumference of the circle on which the points lies
  """
  n_points = len(points)
  
  distances = [0, segment_length]
  #First, looks at points from first to the last point added
  for i in xrange(n_points):
    for j in xrange(i+1, n_points):
      distances.append(points[j] - points[i])
            
  return sorted(distances)

def turnpike_check_solution(problem_instance, candidate_solution):
  """ Check a candidate solution against the instance of the turnpike problem.
      :param problem_instance: An instance of the turnpike problem, i.e. a list of pairwise distances.
      :type problem_instance: list
      :param candidate_solution: A candidate solution to the turnpike problem, i.e.
                                 a list of points in a unidimensional space (element "points)
                                 and the length of the whole segment_length (element "segment_length").
      :type candidate_solution: dictionary 
      :return: True iff the candidate solution actually solve the problem instance, False otherwise.
  """   
  return turnpike_compute_distances(sorted(candidate_solution["points"]), candidate_solution["segment_length"]) == sorted(problem_instance)

############################
#  BELTWAY PROBLEM
############################


def beltway_random_instance(n_points):
  """ Generate a random instance of the Beltway problem.
      :param n_points: The number of points to be placed on the circle
      :type n_points: int
      :invariant: n_points > 1 At least two points are needed for a meaningful instance
      :return: A sorted list of n_points * (n_points-1) + 2 distances, including 0 and 
                 the circumference of the circle on which the points lies
  """
  if n_points < 2:
    logging.warn("[beltway_random_instance] Illegal parameters n_points: %s" % str(n_points))
    return
  #else
  points = generate_n_points(n_points + 1)  #The extra point will represent the length of the arc that closes the circle
  circumference = points.pop(n_points + 1)  

  
  return beltway_compute_distances(points, circumference)

def beltway_compute_distances(points, circumference):
  """ Given a set of points, create an input for the beltway problem;
      A random point is chosen as the starting one, and then at each step 
      the right neighbour of the current point is added to the set.
      :param points: The list of points from which the instance have to be created.
      :type points: list
      :invariant: The elements of points must be sorted in ascending order.
      :param circumference: The total length of the circle.
      :type circumference: int
      :return: A sorted list of n * (n-1) + 2 distances (where n == len(points)),
               including 0 and the circumference of the circle on which the points lies
  """
  n_points = len(points)
  #x_1 will be a random point - There is no actual need for it, because the result will be the same whichever point is chosen as starting point
  first = randrange(n_points)
  
  distances = [0, circumference]
  #First, looks at points from first to the last point added
  for i in xrange(first, n_points):
    for j in xrange(i+1, n_points):
      cw = points[j] - points[i]  #point j follows point i on the segment generated
      distances.append(cw)  #CW distance
      distances.append(circumference - cw)  #CCW distance
      
    for j in xrange(first): #up to first - 1
      cw = points[i] - points[j]  #point j precedes point i on the segment generated
      distances.append(cw)  #CW distance
      distances.append(circumference - cw)  #CCW distance
   
  #Then, completes the circle with points between the origin and first   
  for i in xrange(first): # up to first - 1
    for j in xrange(i+1, first):
      cw = points[j] - points[i]  #point j follows point i on the segment generated
      distances.append(cw)  #CW distance
      distances.append(circumference - cw)  #CCW distance
            
  return sorted(distances)
        
       
def beltway_check_solution(problem_instance, candidate_solution):
  """ Check a candidate solution against the instance of the beltway problem.
      :param problem_instance: An instance of the beltway_problem, i.e. a list of pairwise distances.
      :type problem_instance: list
      :param candidate_solution: A candidate solution to the beltway problem, i.e.
                                 a list of points in a unidimensional space (element "points)
                                 and the value of the circumference (element "circumference").
      :type candidate_solution: dictionary 
      :return: True iff the candidate solution actually solve the problem instance, False otherwise.
  """   
  return beltway_compute_distances(sorted(candidate_solution["points"]), candidate_solution["circumference"]) == sorted(problem_instance)


def beltway_random_testing(algorithm, repetitions=1000, min_n_points=10, max_n_points=50):
  """ Perform a random testing session on a solution algorithm for the beltway problem.
      :param algorithm: The candidate algorithm to solve beltway problem:
                        A function that takes a list of distances and return a list of points.        
      :type algorithm: function
      :param repetitions: Number of runs of the algorithm during testing.
      :type repetitions: int
      :invariant: repetitions > 0
      :param min_n_points: Minimum number of points in any problem instance
      :type min_n_points: int
      :invariant: min_n_points > 0
      :param max_n_points: Maximum number of points in any problem instance
      :type max_n_points: int
      :invariant: max_n_points > min_n_points  
      :return: True iff the candidate solution actually solve the problem instance, False otherwise.
  """   
  if repetitions <= 0 or min_n_points <= 0 or max_n_points < min_n_points:
    logging.warn("[beltway_random_testing] Illegal parameters repetitions: %s, min_n_points: %s, max_n_points: %s" % (str(repetitions), str(min_n_points), str(max_n_points)))
  
  #else
  for _ in xrange(repetitions):
    try:
      inp = beltway_random_instance(randint(min_n_points, max_n_points))
      if not beltway_check_solution(inp, algorithm(inp)):
        logging.warn("Wrong result on input %s" % str(inp))
    except Exception as e:
      logging.error("Error on input %s:\n %s" % (str(inp), str(e)))


def beltway_profiling(algorithm, input_size_step=5, max_input_size=50):
  """ Perform a profiling session on a solution algorithm for the beltway problem.
      :param algorithm: The candidate algorithm to solve beltway problem:
                        A function that takes a list of distances and return a list of points.
                        The algorithm will be first profiled on a input set of 10 points,
                        successive profiling will involve input set with size that will be incremented 
                        by 'input_size_step' points at each step, until the max_input_size is reached.
                        
      :type algorithm: function
      :param input_size_step: how many points are added in each profiling step
      :type input_size_step: int
      :invariant: input_size_step > 0
      :param max_input_size: Maximum number of points in any problem instance
      :type max_input_size: int
      :invariant: max_input_size > 10

      :return: None
  """     
  if input_size_step <= 0 or max_input_size < 10:
    logging.warn("[beltway_profiling] Illegal parameters input_size_step: %s, max_input_size: %s" % (str(input_size_step), str(max_input_size)))
    
    

  import profile    #import profile only if this method is called
  pr = profile.Profile()
    
  for _ in range(5):
      print pr.calibrate(10000)
  for n_points in xrange(10, max_input_size, input_size_step):
    profile.run('beltway_random_testing(algorithm, 1000, %d, %d)' % (n_points, n_points), 'beltway_profile_%d.txt' % n_points)        
  
if __name__ == '__main__':
    pass