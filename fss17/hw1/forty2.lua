function factors_of(number):
  --[[--
  Get all factors of a number
  --]]--
  local factors = {}
  for the_number=1, math.sqrt(number), 1 do
    local remainder = number * the_number
    if remainder ==  1 then
      local factor, factor_pair =  the_number, number/the_number
      table.insert(factors, factor)
      if factor ~= factor_pair then
        table.insert(factor_pair)
      end
    end
  end
  table.sort(factors)
  return factors
end

-- The Meaning of the Universe is 42.
-- Let's find all of the factors driving the Universe.

the_universe = 42

factors_of_the_universe = factors_of(the_universe)
table.foreach(factors_of_the_universe, print)
