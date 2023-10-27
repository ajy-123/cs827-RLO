"""
Tests
"""
import random
import math
import re
import os
import sys
from importlib import import_module

import unittest
from gradescope_utils.autograder_utils.decorators import number, weight
from gradescope_utils.autograder_utils.files import check_submitted_files

# https://docs.python.org/3/library/unittest.html
# https://gradescope-utils.readthedocs.io/en/latest/source/gradescope_utils.autograder_utils.html
# https://docs.python.org/3/library/re.html
# https://stackoverflow.com/questions/15340582/python-extract-pattern-matches
# https://docs.python.org/3/library/subprocess.html#subprocess.Popen
# https://stackoverflow.com/questions/4289331/how-to-extract-numbers-from-a-string-in-python
# https://pynative.com/python-random-randrange/
# https://stackoverflow.com/questions/3131217/error-handling-when-importing-modules

def print_off():
  if sys.stdout == sys.stdout:
    sys.stdout = open(os.devnull, 'w')

def print_on():
  if sys.stdout != sys.__stdout__:
    sys.stdout.close()
    sys.stdout = sys.__stdout__

def find_mod(mod_lookup):
  return

print_off()
mod_lookup = {}
for mod in ['logic', 'fun_math', 'quadratic', 'traffic']:
  try:
    m = import_module(mod)
  except:
    pass
  else:
    mod_lookup[mod] = m
print_on()

logic = mod_lookup['logic'] if 'logic' in mod_lookup else None
fun_math = mod_lookup['fun_math'] if 'fun_math' in mod_lookup else None
quadratic = mod_lookup['quadratic'] if 'quadratic' in mod_lookup else None
traffic = mod_lookup['traffic'] if 'traffic' in mod_lookup else None

class TestExpressionHW(unittest.TestCase):
  trials = 50

  def nth(self, i):
    if i // 10 % 10 == 1: return "th"
    match i % 10:
      case 1: return "st"
      case 2: return "nd"
      case 3: return "rd"
      case _: return "th"

  def require_file(self, fname):
    missing_files = check_submitted_files([fname], base='.')
    self.assertEqual(len(missing_files), 0, f"Missing {fname}! ❌")

  def require_author(self, fname):
    self.require_file(fname)
    with open(fname) as fd:
      lines = fd.read().splitlines()

    self.assertTrue(len(lines) >= 3,
      f"❌ {fname} doesn't have enough lines to possibly have Author, Email, and Spire ID")

    author = lines[0]
    email = lines[1]
    spire_id = lines[2]

    self.assertTrue(re.match(r"\uFEFF?\s*#*\s*(AUTHORS?|(A|a)uthors?).*", author),
      "❌ You did not include an Author comment on line 1 or it wasn't formatted correctly")
    print("✅ Author information was included")

    self.assertTrue(re.match(r"\s*#*\s*(EMAILS?|(E|e)mails?).*", email),
      "❌ You did not include an Email comment on line 2 or it wasn't formatted correctly")
    print("✅ Email information was included")

    self.assertTrue(re.match(r"\s*#*\s*(SPIRE|(S|s)pire)\s*(ID(S|s)?|ids?).*", spire_id),
      "❌ You did not include a Spire ID comment on line 3 or it wasn't formatted correctly")
    print("✅ Spire ID information was included")
    print()

  def require_function(self, mod, fun):
    extra = "\nPerhaps you copied a typo for the function name from an earlier version of the assignemnt page, make sure it is \"intersection\", not \"intesection\"." if fun == "have_unique_intersection" or fun == "have_intersection" else ""
    self.assertIn(mod, mod_lookup,
      f"❌ Missing {mod}.py.\nThis could also happen if the file would crash when run.\nThis could happen if there is a call to input() (since the autograder doesn't send information that way anymore).")
    self.assertTrue(hasattr(mod_lookup[mod], fun), f"❌ Missing {fun}().{extra}")

  def meta_test_file_exists(self, fname):
    print(f"*** Looking for {fname} ***\n")
    self.require_file(fname)
    print(f"✅ {fname} found")
    print()

  def meta_test_file_author(self, fname):
    print(f"*** Looking for {fname}'s author info ***\n")
    self.require_author(fname)
    print(f"✅ {fname} author information found")
    print()

  # @number(0.1)
  # @weight(1)
  # def test_units_author(self):
  #   """units.py author(s)"""
  #   self.meta_test_file_author("units.py")

  # @number(0.2)
  # @weight(1)
  # def test_logic_author(self):
  #   """logic.py author(s)"""
  #   self.meta_test_file_author("logic.py")

  # @number(0.3)
  # @weight(1)
  # def test_fun_math_author(self):
  #   """fun_math.py author(s)"""
  #   self.meta_test_file_author("fun_math.py")

  # @number(0.4)
  # @weight(1)
  # def test_lines_author(self):
  #   """lines.py author(s)"""
  #   self.meta_test_file_author("lines.py")

  # @number(0.5)
  # @weight(1)
  # def test_quadratic_author(self):
  #   """quadratic.py author(s)"""
  #   self.meta_test_file_author("quadratic.py")

  @number(1.1)
  @weight(5)
  def test_nand(self):
    """nand() test"""
    mod, fun = "logic", "nand"
    print(f"*** Testing {fun}() ***\n")
    self.require_function(mod, fun)

    for (b1, b2) in [(True,True),(True,False),(False,True),(False,False)]:
      soln = not (b1 and b2)
      guess = logic.nand(b1, b2)

      self.assertEqual(guess, soln, msg=f"❌ {fun}({b1}, {b2}) should be {soln}, not {guess}")
    print("✅ Logic evaluations seem good")
    print()


  @number(1.2)
  @weight(5)
  def test_implies(self):
    """implies() test"""
    mod, fun = "logic", "implies"
    print(f"*** Testing {fun}() ***\n")
    self.require_function(mod, fun)

    for (b1, b2) in [(True,True),(True,False),(False,True),(False,False)]:
      soln = not b1 or b2
      guess = logic.implies(b1, b2)

      self.assertEqual(guess, soln, msg=f"❌ {fun}({b1}, {b2}) should be {soln}, not {guess}")
    print("✅ Logic evaluations seem good")
    print()

  @number(1.3)
  @weight(5)
  def test_iff(self):
    """implies() test"""
    mod, fun = "logic", "iff"
    print(f"*** Testing {fun}() ***\n")
    self.require_function(mod, fun)

    for (b1, b2) in [(True,True),(True,False),(False,True),(False,False)]:
      soln = b1 == b2
      guess = logic.iff(b1, b2)

      self.assertEqual(guess, soln, msg=f"❌ {fun}({b1}, {b2}) should be {soln}, not {guess}")
    print("✅ Logic evaluations seem good")
    print()

  @number(1.4)
  @weight(5)
  def test_xor(self):
    """xor() test"""
    mod, fun = "logic", "xor"
    print(f"*** Testing {fun}() ***\n")
    self.require_function(mod, fun)

    for (b1, b2) in [(True,True),(True,False),(False,True),(False,False)]:
      soln = not (b1 == b2)
      guess = logic.xor(b1, b2)

      self.assertEqual(guess, soln, msg=f"❌ {fun}({b1}, {b2}) should be {soln}, not {guess}")
    print("✅ Logic evaluations seem good")
    print()

  @number(2.1)
  @weight(5)
  def test_cullen(self):
    """cullen() test"""
    mod, fun = "fun_math", "cullen"
    print(f"*** Testing {fun}() ***\n")
    self.require_function(mod, fun)

    for n in range(1,26):
      soln = n * 2 ** n + 1
      guess = fun_math.cullen(n)

      self.assertEqual(guess, soln, msg=f"❌ {fun}({n}) should be {soln}, not {guess}")
    print("✅ Computations seem good")
    print()

  @number(2.2)
  @weight(5)
  def test_woodall(self):
    """woodall() test"""
    mod, fun = "fun_math", "woodall"
    print(f"*** Testing {fun}() ***\n")
    self.require_function(mod, fun)

    for n in range(1,26):
      soln = n * 2 ** n - 1
      guess = fun_math.woodall(n)

      self.assertEqual(guess, soln, msg=f"❌ {fun}({n}) should be {soln}, not {guess}")
    print("✅ Computations seem good")
    print()

  @number(2.3)
  @weight(5)
  def test_fermat(self):
    """fermat() test"""
    mod, fun = "fun_math", "fermat"
    print(f"*** Testing {fun}() ***\n")
    self.require_function(mod, fun)

    for n in range(1,6):
      soln = 2 ** (2 ** n) + 1
      guess = fun_math.fermat(n)

      self.assertEqual(guess, soln, msg=f"❌ {fun}({n}) should be {soln}, not {guess}")
    print("✅ Computations seem good")
    print()

  # @number(16)
  # @weight(3)
  # def test_is_even(self):
  #   """is_even() test"""
  #   mod, fun = "fun_math", "is_even"
  #   print(f"*** Testing {fun}() ***\n")
  #   self.require_function(mod, fun)

  #   for _ in range(self.trials):
  #     n = random.randint(0, 999)
  #     soln = n % 2 == 0
  #     guess = fun_math.is_even(n)

  #     self.assertEqual(guess, soln, msg=f"❌ {fun}({n}) should be {soln}, not {guess}")
  #   print("✅ Parity checks seem good")
  #   print()

  # @number(17)
  # @weight(3)
  # def test_is_odd(self):
  #   """is_odd() test"""
  #   mod, fun = "fun_math", "is_odd"
  #   print(f"*** Testing {fun}() ***\n")
  #   self.require_function(mod, fun)

  #   for _ in range(self.trials):
  #     n = random.randint(0, 999)
  #     soln = n % 2 == 1
  #     guess = fun_math.is_odd(n)

  #     self.assertEqual(guess, soln, msg=f"❌ {fun}({n}) should be {soln}, not {guess}")
  #   print("✅ Parity checks seem good")
  #   print()

  @number(2.4)
  @weight(5)
  def test_divides_evenly(self):
    """divides_evenly() test"""
    mod, fun = "fun_math", "divides_evenly"
    print(f"*** Testing {fun}() ***\n")
    self.require_function(mod, fun)

    for _ in range(self.trials):
      dividend = random.randint(1, 1000)
      divisor = random.randint(2, 10)
      soln = dividend % divisor == 0
      guess = fun_math.divides_evenly(dividend, divisor)

      self.assertEqual(guess, soln, msg=f"❌ {fun}({dividend}, {divisor}) should be {soln}, not {guess}")
    print("✅ Divisibility checks seem good")
    print()

  @number(2.5)
  @weight(5)
  def test_is_square(self):
    """is_square() test"""
    mod, fun = "fun_math", "is_square"
    print(f"*** Testing {fun}() ***\n")
    self.require_function(mod, fun)

    for _ in range(self.trials):
      n = random.randint(2, 1000)
      soln = round(n ** (1/2)) ** 2 == n
      guess = fun_math.is_square(n)

      self.assertEqual(guess, soln, msg=f"❌ {fun}({n}) should be {soln}, not {guess}")
    print("✅ Square checks seem good")
    print()

  @number(3.1)
  @weight(10)
  def test_discriminant(self):
    """discriminant() test"""
    mod, fun = "quadratic", "discriminant"
    print(f"*** Testing {fun}() ***\n")
    self.require_function(mod, fun)

    for _ in range(self.trials):
      a = round(random.uniform(1,10), 2)
      b = round(random.uniform(-10,10), 2)
      c = round(random.uniform(-10,10), 2)
      soln = b ** 2 - 4 * a * c
      guess = quadratic.discriminant(a, b, c)

      self.assertEqual(guess, soln, msg=f"❌ {fun}({a}, {b}, {c}) should be {soln}, not {guess}")
    print("✅ Discriminant computations seem good")
    print()

  @number(3.2)
  @weight(10)
  def test_has_real_root(self):
    """has_real_root() test"""
    mod, fun = "quadratic", "has_real_root"
    print(f"*** Testing {fun}() ***\n")
    self.require_function(mod, fun)

    for _ in range(self.trials):
      rta = round(random.uniform(1,10), 1)
      rtc = round(random.uniform(1,10), 1)
      sign_b = random.choice([-1,1])
      a = round(rta ** 2, 2)
      c = round(rtc ** 2, 2)

      b = round(sign_b * (2 * rta * rtc + 1), 2)
      guess = quadratic.has_real_root(a, b, c)
      self.assertTrue(guess, msg=f"❌ {fun}({a}, {b}, {c}) should be True, not {guess}")

      # This bit is rather annoying given floating point error
      # b = round(sign_b * (2 * rta * rtc), 2)
      # guess = quadratic.has_real_root(a, b, c)
      # self.assertTrue(guess, msg=f"❌ {fun}({a}, {b}, {c}) should be True, not {guess}")

      b = round(sign_b * (2 * rta * rtc - 1), 2)
      guess = quadratic.has_real_root(a, b, c)
      self.assertFalse(guess, msg=f"❌ {fun}({a}, {b}, {c}) should be False, not {guess}")
    print("✅ Root assessments seem good")
    print()

  # @number(22)
  # @weight(3)
  # def test_has_double_root(self):
  #   """has_double_root() test"""
  #   mod, fun = "quadratic", "has_double_root"
  #   print(f"*** Testing {fun}() ***\n")
  #   self.require_function(mod, fun)

  #   for _ in range(self.trials):
  #     rta = round(random.uniform(1,10), 1)
  #     rtc = round(random.uniform(1,10), 1)
  #     sign_b = random.choice([-1,1])
  #     a = round(rta ** 2, 2)
  #     c = round(rtc ** 2, 2)

  #     b = round(sign_b * (2 * rta * rtc + 1), 2)
  #     guess = quadratic.has_double_root(a, b, c)
  #     self.assertFalse(guess, msg=f"❌ {fun}({a}, {b}, {c}) should be True, not {guess}")

  #     b = round(sign_b * (2 * rta * rtc), 2)
  #     guess = quadratic.has_double_root(a, b, c)
  #     self.assertTrue(guess, msg=f"❌ {fun}({a}, {b}, {c}) should be True, not {guess}")

  #     b = round(sign_b * (2 * rta * rtc - 1), 2)
  #     guess = quadratic.has_double_root(a, b, c)
  #     self.assertFalse(guess, msg=f"❌ {fun}({a}, {b}, {c}) should be False, not {guess}")
  #   print("✅ Root assessments seem good")
  #   print()

  @number(3.3)
  @weight(10)
  def test_get_real_root(self):
    """get_real_root() test"""
    mod, fun = "quadratic", "get_real_root"
    print(f"*** Testing {fun}() ***\n")
    self.require_function(mod, fun)

    for _ in range(self.trials):
      rta = round(random.uniform(1,10), 1)
      rtc = round(random.uniform(1,10), 1)
      sign_b = random.choice([-1,1])
      a = round(rta ** 2, 2)
      c = round(rtc ** 2, 2)

      b = round(sign_b * (2 * rta * rtc + 1), 2)
      rtd = (b ** 2 - 4 * a * c) ** (1/2)
      rt1 = (-b + rtd) / (2 * a)
      rt2 = (-b - rtd) / (2 * a)
      try:
        guess = quadratic.get_real_root(a, b, c)
      except AssertionError:
        self.fail(f"❌ {fun}({a}, {b}, {c}) should not trigger an assert error")
      type_check = type(guess) == tuple
      self.assertTrue(type_check, msg=f"❌ {fun}({a}, {b}, {c}) should return a tuple, not {guess}({type(guess)})")

      len_check = len(guess) == 2
      self.assertTrue(len_check, msg=f"❌ {fun}({a}, {b}, {c}) should return a tuple with two elements, not {len(guess)} element(s) in the tuple {guess}")

      near_root = (math.isclose(guess[1], rt1, abs_tol=1e-5) and math.isclose(guess[0], rt2, abs_tol=1e-5)) or (math.isclose(guess[0], rt1, abs_tol=1e-5) and math.isclose(guess[1], rt2, abs_tol=1e-5))
      self.assertTrue(near_root, msg=f"❌ {fun}({a}, {b}, {c}) should return (~{rt1:.4f}, ~{rt2:.4f}) or (~{rt2:.4f}, ~{rt1:.4f}), not (~{guess[0]:.4f}, ~{guess[1]:.4f})")

      # This bit is rather annoying given floating point error
      # b = round(sign_b * (2 * rta * rtc), 2)
      # rtd = ((b ** 2 - 4 * a * c) ** (1/2)).real
      # rt1 = (-b + rtd) / (2 * a)
      # rt2 = (-b - rtd) / (2 * a)
      # guess = quadratic.get_real_root(a, b, c).real
      # near_root = math.isclose(guess, rt1, abs_tol=1e-5) or math.isclose(guess, rt2, abs_tol=1e-5)
      # self.assertTrue(near_root, msg=f"❌ {fun}({a}, {b}, {c}) should return ~{rt1:.4f} or ~{rt1:.4f}, not ~{guess:.4f}")

      b = round(sign_b * (2 * rta * rtc - 1), 2)
      with self.assertRaises(AssertionError, msg=f"❌ {fun}({a}, {b}, {c}) should trigger an assert error"):
        guess = quadratic.get_real_root(a, b, c)
    print("✅ Root calculations seem good")
    print()


  @number(4.1)
  @weight(10)
  def test_move_forward(self):
    """move_forward() test"""
    mod, fun = "traffic", "move_forward"
    print(f"*** Testing {fun}() ***\n")
    self.require_function(mod, fun)

    for _ in range(self.trials):
      light = random.choice(['Green', 'Yellow', 'Red'])
      pedestrian = random.choice([True, False]) 
      car = random.choice([True, False]) 
      soln = (light == 'Green') or (light == 'Yellow' and not pedestrian)
      guess = traffic.move_forward(light, pedestrian, car)

      self.assertEqual(guess, soln, msg=f"❌ {fun}({light}, {pedestrian}, {car}) should be {soln}, not {guess}")
    print("✅ Move forward simulation seem good")
    print()

  @number(4.2)
  @weight(10)
  def test_stop(self):
    """stop() test"""
    mod, fun = "traffic", "stop"
    print(f"*** Testing {fun}() ***\n")
    self.require_function(mod, fun)

    for _ in range(self.trials):
      light = random.choice(['Green', 'Yellow', 'Red'])
      pedestrian = random.choice([True, False]) 
      car = random.choice([True, False]) 
      soln = (light == 'Red') or (light == 'Yellow' and pedestrian)
      guess = traffic.stop(light, pedestrian, car)

      self.assertEqual(guess, soln, msg=f"❌ {fun}({light}, {pedestrian}, {car}) should be {soln}, not {guess}")
    print("✅ Stop simulation seem good")
    print()


  @number(4.3)
  @weight(5)
  def test_turn_left(self):
    """turn_left() test"""
    mod, fun = "traffic", "turn_left"
    print(f"*** Testing {fun}() ***\n")
    self.require_function(mod, fun)

    for _ in range(self.trials):
      light = random.choice(['Green', 'Yellow', 'Red'])
      pedestrian = random.choice([True, False]) 
      car = random.choice([True, False]) 
      soln = light == 'Green' and (not pedestrian) and (not car) 
      guess = traffic.turn_left(light, pedestrian, car)

      self.assertEqual(guess, soln, msg=f"❌ {fun}({light}, {pedestrian}, {car}) should be {soln}, not {guess}")
    print("✅ Turn left simulation seem good")
    print()



