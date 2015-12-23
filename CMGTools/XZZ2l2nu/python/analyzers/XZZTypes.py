from CMGTools.XZZ2l2nu.analyzers.AutoFillTreeProducer  import * 



LLType = NTupleObjectType("LLType", baseObjectTypes=[fourVectorType], variables = [
    NTupleVariable("mt",   lambda x : x.mt(), float),       
    NTupleVariable("deltaPhi",   lambda x : x.deltaPhi(), float),       
    NTupleVariable("deltaR",   lambda x : x.deltaR(), float),       
])



VVType = NTupleObjectType("VVType", baseObjectTypes=[], variables = [
  NTupleSubObject("LV",  lambda x : x['pair'],fourVectorType),
  NTupleVariable("deltaPhi",   lambda x : x['pair'].deltaPhi(), float),       
  NTupleVariable("deltaR",   lambda x : x['pair'].deltaR(), float),       
  NTupleVariable("mt",   lambda x : x['pair'].mt(), float),       
])


LLNuNuType = NTupleObjectType("LLNuNuType", baseObjectTypes=[VVType], variables = [
    NTupleSubObject("l1",  lambda x : x['pair'].leg1,LLType),
    NTupleSubObject("l1_l1",  lambda x : x['pair'].leg1.leg1,leptonTypeExtra),
    NTupleSubObject("l1_l2",  lambda x : x['pair'].leg1.leg2,leptonTypeExtra),
    NTupleSubObject("l2",  lambda x : x['pair'].leg2,metType),
])

