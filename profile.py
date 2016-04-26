import cProfile, pstats

def profile(python_string):
  cProfile.run(python_string, 'profile_results.txt')
  p = pstats.Stats('profile_results.txt')
  p.strip_dirs().sort_stats('cumulative').print_stats(10)
  os.remove('profile_results.txt')
