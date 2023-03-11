absInt :: Int -> Int
absInt n | n > 0 = n
         | otherwise = -n

sgn :: Int -> Int
sgn n | n > 0 = 1
      | n < 0 = -1
      | otherwise = 0

min3Int :: (Int, Int, Int) -> Int
min3Int (n, k, l) | n <= k && n <= l = n
                  | k <= n && k <= l = k
                  | otherwise = l
