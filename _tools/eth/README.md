# Amharic and Afaan Oromo translations

The site (`index.html`) holds the Amharic (`am`) and Afaan Oromo (`om`) recipe text in one injected object, between `/*ETH*/const ETH=` and `/*ETHEND*/`. `integrate.py` keeps every translation already in that object and adds new ones from text files.

## Steps for new recipes

1. Export what is missing:
   `python3 _tools/eth/export_missing.py index.html /tmp/eth/en_new.txt`
   It prints the missing recipe ids. If the list is empty, stop.
2. Translate `/tmp/eth/en_new.txt` into `/tmp/eth/am_new.txt` (Amharic) and `/tmp/eth/om_new.txt` (Afaan Oromo).
   - Keep exactly the same lines and line types. Translate only the text after the marker.
   - Keep numbers, units and brand names. Don't use `ነጭ ሽንኩርት` (garlic) for onion.
3. Check that the structure matches. Each command must print OK:
   `python3 _tools/eth/check.py /tmp/eth/en_new.txt /tmp/eth/am_new.txt`
   `python3 _tools/eth/check.py /tmp/eth/en_new.txt /tmp/eth/om_new.txt`
4. Merge into the page:
   `python3 _tools/eth/integrate.py index.html /tmp/eth`
   It must print `missing []`.
5. Commit and push.

## File format

| Line | Meaning |
|---|---|
| `@id \| title` | recipe |
| `= heading` | ingredients block, followed by `- item` lines |
| `+ heading` | steps block, followed by `> step` lines |

Notes are not translated.
