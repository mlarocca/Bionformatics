'''
Created on 09/nov/2013

@author: mlarocca
'''
import unittest

from beltway_turnpike_test_suite import beltway_compute_distances, generate_n_points, turnpike_compute_distances, beltway_check_solution, turnpike_check_solution
from random import randrange

class Test(unittest.TestCase):

  def test_bealtway_instance_generator(self):
    for _ in xrange(20):
      d = beltway_compute_distances([0, 3, 8, 11], 13)
      try:
        assert d == [0, 2, 3, 3, 5, 5 , 5, 8, 8, 8, 10, 10, 11, 13]
      except AssertionError as e:
        print d
        raise e
      d1 = beltway_compute_distances([1, 4, 9, 12], 13)
      try:
        assert d == d1
      except AssertionError as e:
        print d
        raise e   
    
    #since there is a random factor in beltway_compute_distances, it's appropriate a test that shows the result is exactly the same
    for _ in xrange(20):
      n_points = randrange(1, 50)
      points = generate_n_points(n_points + 1)
      circumference = points.pop(n_points + 1)

      assert len(beltway_compute_distances(points, circumference)) == n_points * (n_points + 1) + 2      ### n == (n_points + 1) => == n * (n-1) + 2
      assert beltway_compute_distances(points, circumference) == beltway_compute_distances(points, circumference)

  def test_random_point_generator(self):
    for _ in xrange(20):
      points = generate_n_points(randrange(1, 50))
      assert(0 in points)
      assert(points == sorted(points))   
      
  def test_turnpike_istance_generator(self):
    assert  turnpike_compute_distances([0, 1, 9, 13], 15) == [0, 1, 4, 8, 9, 12, 13, 15]
    
    for _ in xrange(20):
      n_points = randrange(1, 50)    
      points = generate_n_points(n_points + 1)
      segment_length = points.pop(n_points + 1)   
      assert len(turnpike_compute_distances(points, segment_length)) == n_points * (n_points + 1) / 2 + 2 ### n == (n_points + 1) => == n * (n-1) / 2  + 2
    
  def test_beltway_check_solution(self):
    for _ in xrange(20):
      n_points = randrange(1, 50)
      points = generate_n_points(n_points + 1)
      circumference = points.pop(n_points + 1)
      #check True on valid solution
      assert beltway_check_solution(beltway_compute_distances(points, circumference), {"circumference": circumference, "points": points})
      #check False on wrong solutions
      tmp = points[:]
      tmp.pop(randrange(n_points))
      assert not beltway_check_solution(beltway_compute_distances(points, circumference), {"circumference": circumference, "points": tmp})
      
      tmp = points[:]
      tmp.append(randrange(n_points))
      assert not beltway_check_solution(beltway_compute_distances(points, circumference), {"circumference": circumference, "points": tmp})      

  def test_turnpike_check_solution(self):
    for _ in xrange(20):
      n_points = randrange(1, 50)
      points = generate_n_points(n_points + 1)
      segment_length = points.pop(n_points + 1)
      #check True on valid solution
      assert turnpike_check_solution(turnpike_compute_distances(points, segment_length), {"segment_length": segment_length, "points": points})
      #check False on wrong solutions
      tmp = points[:]
      tmp.pop(randrange(n_points))
      assert not turnpike_check_solution(turnpike_compute_distances(points, segment_length), {"segment_length": segment_length, "points": tmp})

if __name__ == "__main__":
  #import sys;sys.argv = ['', 'Test.testName']
  unittest.main()