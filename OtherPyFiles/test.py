import re

_d = {
    "1": ["Адское возмездие [Hellish rebuke]"],
    "2": ["Адское возмездие [Hellish rebuke]"],
    "0": ["123"],
}
print([i for k in _d for i in _d[k]])
