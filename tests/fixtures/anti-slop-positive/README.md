# Anti-AI-slop NEGATIVE fixture (positive findings)

This directory deliberately contains the seven cardinal AI-slop sins so the
`design-audit` rule pack can prove it catches them. Tests assert that running
`design-audit` on this directory returns findings; an audit that returns 0
findings here is itself a regression.

⚠️  Do not import or render the files in this directory in any production
context — they are intentionally broken samples for test only.
