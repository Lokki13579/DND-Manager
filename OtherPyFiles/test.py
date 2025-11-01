import re

pattern = r"(\([1-9аговорЗз]\))?([^\(][^#]+[^)])?"

string = "(1) Адское возмездие [Hellish rebuke]"
string = "(2)"
string = "Адское возмездие [Hellish rebuke]"
string = "(Заговор) [Spell]"

print(re.findall(pattern, string))
