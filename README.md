#acsm
Aho-Corasick String Match.

A python implementation of aho-corasick string searching algorithm.

----------
##Usage
```python
import acsm
string_match = acsm.StringMatch()
pattern_list = ["java", "c", "c++", "python"]
string_match.read_from_iterable(pattern_list)
print(string_match.match("Python is awesome", True))
```
