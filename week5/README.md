1.to create nwe project 
```text
uv init
```
2.to add fast api
```text
uv add "fastapi[standard]"
```
3.to start fast api
```text
uv run fastapi dev
```
4.if port is already running
```text
lsof -i :8000      #(port ko name)
kill -9 pid      #(number deko hunchha)
```