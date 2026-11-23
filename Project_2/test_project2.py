from pathlib import Path
import unittest
from portfolio import benchmark,equal_weight,evaluate,load_estimates,optimize,validate_inputs,verdict
from lly_dcf import BASE_CASE, build, valuation
ROOT=Path(__file__).resolve().parent
class ProjectTests(unittest.TestCase):
 @classmethod
 def setUpClass(c): c.s,c.c=load_estimates(ROOT/'data'/'prices_through_2026-10-19.csv')
 def test_baselines_explain_failures(self):
  self.assertIn('return objective',verdict(evaluate(equal_weight(self.s),self.s,self.c)))
  self.assertIn('reserve minimum',verdict(evaluate(benchmark(self.s),self.s,self.c)))
 def test_constrained_passes(self): self.assertEqual(verdict(optimize(self.s,self.c)),'PASS')
 def test_stress_increases_risk(self): self.assertGreater(optimize(self.s,self.c,.075)['volatility'],optimize(self.s,self.c)['volatility'])
 def test_estimate_haircut_and_cost_reduce_return(self):
  haircut_s,_=load_estimates(ROOT/'data'/'prices_through_2026-10-19.csv', return_haircut=.01)
  self.assertLess(optimize(haircut_s,self.c)['return'],optimize(self.s,self.c)['return'])
  self.assertLess(evaluate(optimize(self.s,self.c)['weights'],self.s,self.c,.0025)['return'],optimize(self.s,self.c)['return'])
 def test_shorter_window_is_reproducible(self):
  short_s,short_c=load_estimates(ROOT/'data'/'prices_through_2026-10-19.csv', lookback_months=36)
  self.assertIsNotNone(optimize(short_s,short_c))
 def test_no_feasible_mix_is_explicit(self):
  self.assertIsNone(optimize(self.s,self.c,.50,.90))
 def test_invalid_correlation_is_refused(self):
  bad={left:dict(row) for left,row in self.c.items()}; bad['VTI']['LQD']=bad['LQD']['VTI']=1.2
  with self.assertRaisesRegex(ValueError,'within'):
   validate_inputs(self.s,bad)
 def test_lab14_course_known_answer_reconciles(self):
  sleeves={'BIL':{'return':.035,'volatility':.005},'IEF':{'return':.043,'volatility':.070},'LQD':{'return':.050,'volatility':.060},'VTI':{'return':.080,'volatility':.160}}
  corr={'BIL':{'BIL':1,'IEF':.10,'LQD':.05,'VTI':0},'IEF':{'BIL':.10,'IEF':1,'LQD':.80,'VTI':-.10},'LQD':{'BIL':.05,'IEF':.80,'LQD':1,'VTI':.25},'VTI':{'BIL':0,'IEF':-.10,'LQD':.25,'VTI':1}}
  result=evaluate({'BIL':0,'IEF':0,'LQD':.40,'VTI':.60},sleeves,corr)
  self.assertAlmostEqual(result['return'],.0680,places=4)
  self.assertAlmostEqual(result['volatility'],.1046,places=4)
  self.assertAlmostEqual(result['reserve'],0,places=4)
 def test_llY_dcf_known_base_reconciliation(self):
  self.assertAlmostEqual(valuation(build(BASE_CASE), BASE_CASE.wacc, BASE_CASE.terminal_growth)['per_share'], 637.42, places=2)
if __name__=='__main__': unittest.main(verbosity=2)
