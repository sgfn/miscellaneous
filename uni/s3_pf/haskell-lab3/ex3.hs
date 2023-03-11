sqr x = x^2

funcfactory n = case n of
    1 -> id
    2 -> sqr
    3 -> (^3)
    4 -> \x -> x^4
    5 -> intFunc
    _ -> const n
    where
        intFunc x = x ^ 5


--factorial :: Int -> Double
--factorial 0 = 1
--factorial x = if x > 0 then x * factorial (x-1) else 0

addfunc :: Num a => (a -> a) -> (a -> a) -> a -> a
addfunc f g applyon = f applyon + g applyon

eaut :: Int -> Double -> Double
--eaut 0 = \x -> 1
--eaut n = if n > 0 && n <= 6 then addfunc (\x -> (x^n)/(factorial n)) (eaut n-1) else id

eaut n = case n of
    0 -> const 1
    1 -> addfunc (eaut 0) (id)
    2 -> addfunc (eaut 1) (\x -> x^2/2)
    3 -> addfunc (eaut 2) (\x -> x^3/6)
    4 -> addfunc (eaut 3) (\x -> x^4/24)
    5 -> addfunc (eaut 4) (\x -> x^5/120)
    _ -> const 1
