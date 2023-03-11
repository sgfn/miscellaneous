not' :: Bool -> Bool
not' b = case b of
            True -> False
            False -> True

abs' :: Int -> Int
abs' n = case (n >= 0) of
            True -> n
            _ -> -n
