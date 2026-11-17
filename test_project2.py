from pathlib import Path
import unittest
from portfolio import benchmark,equal_weight,evaluate,load_estimates,optimize,verdict
ROOT=Path(__file__).resolve().parent
class ProjectTests(unittest.TestCase):
 @classmethod
 def setUpClass(c): c.s,c.c=load_estimates(ROOT/'data'/'prices_through_2026-10-19.csv')
 def test_baselines_explain_failures(self):
  self.assertIn('return objective',verdict(evaluate(equal_weight(self.s),self.s,self.c)))
  self.assertIn('reserve minimum',verdict(evaluate(benchmark(self.s),self.s,self.c)))
 def test_constrained_passes(self): self.assertEqual(verdict(optimize(self.s,self.c)),'PASS')
 def test_stress_increases_risk(self): self.assertGreater(optimize(self.s,self.c,.075)['volatility'],optimize(self.s,self.c)['volatility'])
if __name__=='__main__': unittest.main(verbosity=2)
