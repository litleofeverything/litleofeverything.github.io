# Translating new recipes: Amharic, Afaan Oromo and Filipino

The site (`index.html`) holds the translated recipe text in one data object, between `/*ETH*/const ETH=` and `/*ETHEND*/`. The languages are:

- `am`: Amharic
- `om`: Afaan Oromo
- `tl`: Filipino (Tagalog)

`integrate.py` keeps every translation that is already there and replaces only that data object. The language buttons are already in the page.

## Steps for new recipes

1. Export what is missing:
   `python3 _tools/eth/export_missing.py index.html /tmp/eth/en_new.txt`
   It prints the missing ids for each language. If it prints `missing []`, stop.
2. Translate `/tmp/eth/en_new.txt` into the languages that are missing:
   - `/tmp/eth/am_new.txt` (Amharic)
   - `/tmp/eth/om_new.txt` (Afaan Oromo)
   - `/tmp/eth/tl_new.txt` (Filipino)

   Keep exactly the same lines and line types, and translate only the text after the marker. Keep numbers and units. Don't write `ነጭ ሽንኩርት` (garlic in Amharic) where the recipe means onion.
3. Check each file. Each command must print OK:
   `python3 _tools/eth/check.py /tmp/eth/en_new.txt /tmp/eth/am_new.txt` (and the same for `om_new.txt` and `tl_new.txt`)
4. Merge into the page:
   `python3 _tools/eth/integrate.py index.html /tmp/eth`
   It must print `missing []`.
5. Commit and push. Change nothing else in the page.

## File format

| Line | Meaning |
|---|---|
| `@id \| title` | recipe |
| `= heading` | ingredients block, followed by `- item` lines |
| `+ heading` | steps block, followed by `> step` lines |

Notes are not translated.
