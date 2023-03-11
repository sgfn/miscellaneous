sgn :: Int -> Int
sgn n = if n < 0
        then -1
        else if n == 0
             then 0
             else 1

absInt :: Int -> Int
absInt n = if n < 0
           then (-n)
           else n

min2Int :: (Int, Int) -> Int
min2Int (n, k) = if n < k
                 then n
                 else k

min3Int :: (Int, Int, Int) -> Int
min3Int (n, k, l) = min2Int (min2Int (n, k), min2Int (k, l))
