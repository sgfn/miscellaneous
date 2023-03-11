mysum :: Num a => [a] -> a
mysum [] = 0
mysum (x:xs) = x + mysum xs

sumsqr :: Num a => [a] -> a
sumsqr [] = 0
sumsqr (x:xs) = x*x + sumsqr xs

sumwith :: Num a => (a -> a) -> [a] -> a
sumwith f [] = 0
sumwith f (x:xs) = f x + sumwith f xs

dowith :: Num a => (a -> a -> a) -> a -> (a -> a) -> [a] -> a
dowith g def f [] = def
dowith g def f (x:xs) = g (f x) (dowith g def f xs)

dowith0 :: Num a => (a -> a -> a) -> (a -> a) -> [a] -> a
dowith0 g f l = dowith g 0 f l

newsumwith :: (Num a, Floating b) => (a -> b) -> [a] -> b
newsumwith f [] = 0
newsumwith f (x:xs) = f x + newsumwith f xs
