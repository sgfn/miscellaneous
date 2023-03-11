not' :: Bool -> Bool
not' True = False
not' False = True

testFun :: String -> Bool
testFun "aaaa" = True
testFun _      = False

or' :: (Bool, Bool) -> Bool
or' (False, False) = False
or' _ = True

and' :: (Bool, Bool) -> Bool
and' (True, True) = True
and' _ = False

nand' :: (Bool, Bool) -> Bool
nand' (True, True) = False
nand' _ = True

xor' :: (Bool, Bool) -> Bool
xor' (False, False) = True
xor' (True, True) = True
xor' _ = False
