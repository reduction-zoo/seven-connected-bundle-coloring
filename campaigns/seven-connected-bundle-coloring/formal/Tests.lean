import Challenge
open SevenConnectedBundleColoring
example : legalSource (⟨1,[]⟩,[[]]) = true := by native_decide
example : sourceWitness (⟨1,[]⟩,[[]]) [1] = false := by native_decide
example : legalTarget ⟨⟨7,[]⟩,[0,1,2,3,4,5,6]⟩ = true := by native_decide
example : targetWitness ⟨⟨7,[]⟩,[0,1,2,3,4,5,6]⟩ [1,1,1,1,1,1,1] = true := by native_decide
