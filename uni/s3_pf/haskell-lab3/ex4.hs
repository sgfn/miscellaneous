import Data.List
import Data.Char

sortDesc :: Ord a => [a] -> [a]
sortDesc xs = (reverse . sort) xs

sdpf xs = reverse (sort (xs))


a2fea :: Eq a => (t -> a) -> (t -> a) -> [t] -> Bool
a2fea f g xs = foldr (&&) True (map (eqfun) xs)
    where eqfun x = f x == g x


onlyeven [] = []
onlyeven (x:xs)
    | x `mod` 2 == 0 = x : onlyeven xs
    | otherwise      = onlyeven xs

onlyupper [] = []
onlyupper (x:xs)
    | isUpper x = x : onlyupper xs
    | otherwise = onlyupper xs

myfilter :: (a -> Bool) -> [a] -> [a]
myfilter pred [] = []
myfilter pred (x:xs)
    | pred x    = x : (myfilter pred xs)
    | otherwise = myfilter pred xs
