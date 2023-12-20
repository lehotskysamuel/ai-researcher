# TODO

1) Doplnit cb do metadata

lords of silence
```
# Tokens Used: 173853
# 	Prompt Tokens: 159691
# 	Completion Tokens: 14162
# Successful Requests: 47
# Total Cost (USD): $2.02177
# 
# Process finished with exit code 0
```

avenging son
```
Tokens Used: 256431
	Prompt Tokens: 234307
	Completion Tokens: 22124
Successful Requests: 59
Total Cost (USD): $3.00679

Process finished with exit code 0
```


2) refactor

- samostatna classa na metadata (a ta bude mat dump a load metody, takze vobec nebudem musiet riesit json)
- pouzit tu triedu aj v streamlit - tlacitka by mali obsahovat title a nie folder name (takze musim nacitat metadata)
- vycistit kod: lint, isort atd



## Next:
- lepsi error handling, task retry
- toggle, kde si zapnem a vypnem irelevantne kapitoly
- form na jednotlive kroky (stranka pre import knihy)
- progress bar, nejaky framework na task batching
- utils pre streamlit
- utils pre subory zvlast
- utils pre paths - spravit konstanty pre vsetky data directories
